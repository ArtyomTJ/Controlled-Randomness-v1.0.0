// Controlled Randomness — reference implementation (C++17).
//
// This program is a faithful port of the original selection algorithm and
// adds a control arm. It is intentionally dependency-free so that it can be
// built anywhere:
//
//   g++ -std=c++17 -O2 -Wall -Wextra -o cr controlled_randomness.cpp
//   ./cr --self-test
//   ./cr --arm both --target 17 19 --trials 10000
//
// The program demonstrates the causal-isolation result: for a fixed seed,
// the control and selection arms execute the same draw sequence and stop at
// the same iteration. See docs/MATH.md for the proof.

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

class MsvcRand {
public:
    explicit MsvcRand(std::uint32_t seed) : state_(seed) {}

    int next() {
        state_ = static_cast<std::uint32_t>(state_ * 214013u + 2531011u);
        return static_cast<int>((state_ >> 16) & 0x7FFFu);
    }

    int pair_value(int lo, int hi) {
        const int span = hi - lo + 1;
        return (next() % span) + lo;
    }

private:
    std::uint32_t state_;
};

// The original selection rule. It updates only the auxiliary pair (x, y).
// The stopping predicate and the RNG are untouched.
void update_selection(int& x, int& y, int a, int b, int c, int d) {
    if (c > 0 && d > 0) {
        if ((x < 0 && y < 0 && a > 0 && b > 0) ||
            (x < 0 && y < 0 && ((a < 0 && b > 0) || (a > 0 && b < 0))) ||
            (a > 0 && b > 0 && ((x < 0 && y > 0) || (x > 0 && y < 0))) ||
            (((x < 0 && y > 0) || (x > 0 && y < 0)) &&
             ((a < 0 && b > 0) || (a > 0 && b < 0))) ||
            (x == 0 || y == 0)) {
            x = a;
            y = b;
        }
        if ((x > 0 && y > 0 && a > 0 && b > 0) &&
            (std::abs(((c + d) / 2.0) - ((x + y) / 2.0)) >
             std::abs(((c + d) / 2.0) - ((a + b) / 2.0)))) {
            x = a;
            y = b;
        }
    } else {
        if ((x > 0 && y > 0 && a < 0 && b < 0) ||
            (x > 0 && y > 0 && ((a < 0 && b > 0) || (a > 0 && b < 0))) ||
            (a < 0 && b < 0 && ((x < 0 && y > 0) || (x > 0 && y < 0))) ||
            (((x < 0 && y > 0) || (x > 0 && y < 0)) &&
             ((a < 0 && b > 0) || (a > 0 && b < 0))) ||
            (x == 0 || y == 0)) {
            x = a;
            y = b;
        }
        if ((x < 0 && y < 0 && a < 0 && b < 0) &&
            (std::abs(((std::abs(c) + std::abs(d)) / 2.0) -
                      ((std::abs(x) + std::abs(y)) / 2.0)) >
             std::abs(((std::abs(c) + std::abs(d)) / 2.0) -
                      ((std::abs(a) + std::abs(b)) / 2.0)))) {
            x = a;
            y = b;
        }
    }
}

struct TrialResult {
    long long iterations;
    int final_x;
    int final_y;
};

TrialResult run_trial(bool use_selection, std::uint32_t seed, int c, int d,
                      int lo, int hi) {
    MsvcRand rng(seed);
    int a = 1;
    int b = 1;
    int x = 1;
    int y = 1;
    long long iterations = 0;

    while (!(a == c && b == d)) {
        a = rng.pair_value(lo, hi);
        b = rng.pair_value(lo, hi);
        ++iterations;
        if (use_selection) {
            update_selection(x, y, a, b, c, d);
        }
    }

    return {iterations, x, y};
}

double value_prob_msvc(int v, int lo, int hi) {
    const int span = hi - lo + 1;
    const int residue = v - lo;
    const int base = 32768 / span;
    const int rem = 32768 % span;
    return static_cast<double>(base + (residue < rem ? 1 : 0)) / 32768.0;
}

double target_prob(int c, int d, int lo, int hi) {
    return value_prob_msvc(c, lo, hi) * value_prob_msvc(d, lo, hi);
}

struct Stats {
    long long n = 0;
    double mean = 0.0;
    double sd = 0.0;
    long long min = 0;
    long long max = 0;
};

Stats summarize(const std::vector<long long>& values) {
    if (values.empty()) {
        throw std::runtime_error("cannot summarize an empty sequence");
    }
    long double sum = 0.0L;
    for (long long value : values) {
        sum += static_cast<long double>(value);
    }
    const long double mean = sum / static_cast<long double>(values.size());
    long double squares = 0.0L;
    for (long long value : values) {
        const long double diff = static_cast<long double>(value) - mean;
        squares += diff * diff;
    }
    Stats stats;
    stats.n = static_cast<long long>(values.size());
    stats.mean = static_cast<double>(mean);
    stats.sd = values.size() > 1
                   ? std::sqrt(static_cast<double>(squares /
                                                   static_cast<long double>(values.size() - 1)))
                   : 0.0;
    stats.min = *std::min_element(values.begin(), values.end());
    stats.max = *std::max_element(values.begin(), values.end());
    return stats;
}

struct Options {
    std::string arm = "both";
    int c = 17;
    int d = 19;
    long long trials = 1000;
    std::uint32_t seed = 1000003u;
    int lo = -20;
    int hi = 20;
    std::string out;
    bool self_test = false;
};

void print_usage() {
    std::cout
        << "Usage:\n"
        << "  cr --arm both --target C D --trials N [--seed S] [--lo L] [--hi H] [--out FILE]\n"
        << "  cr --arm control|select --target C D --trials N [options]\n"
        << "  cr --self-test\n";
}

bool self_test() {
    if (MsvcRand(1).next() != 41) {
        std::cerr << "self-test failed: MSVC rand(1) != 41\n";
        return false;
    }

    struct Case {
        int x;
        int y;
        int a;
        int b;
        int c;
        int d;
        int expected_x;
        int expected_y;
    };
    const Case cases[] = {
        {-5, -5, 3, 4, 10, 12, 3, 4},
        {-5, 5, 3, 4, 10, 12, 3, 4},
        {3, 4, -5, 5, 10, 12, 3, 4},
        {3, -4, -5, 6, 10, 12, -5, 6},
        {3, 4, 5, 6, 10, 12, 5, 6},
        {5, 6, 3, 4, 10, 12, 5, 6},
        {5, 5, -3, -4, -10, -12, -3, -4},
        {-3, -4, -5, -6, -10, -12, -5, -6},
        {0, 5, -3, 4, 10, 12, -3, 4},
    };

    for (const Case& item : cases) {
        int x = item.x;
        int y = item.y;
        update_selection(x, y, item.a, item.b, item.c, item.d);
        if (x != item.expected_x || y != item.expected_y) {
            std::cerr << "self-test failed: selection rule case\n";
            return false;
        }
    }

    for (std::uint32_t seed = 0; seed < 200; ++seed) {
        const TrialResult control = run_trial(false, seed, 3, 4, -5, 5);
        const TrialResult selection = run_trial(true, seed, 3, 4, -5, 5);
        if (control.iterations != selection.iterations) {
            std::cerr << "self-test failed: paired mismatch at seed " << seed << "\n";
            return false;
        }
    }

    std::cout << "self-test OK\n";
    return true;
}

int parse_int(const std::string& text) {
    try {
        std::size_t consumed = 0;
        const int value = std::stoi(text, &consumed);
        if (consumed != text.size()) {
            throw std::invalid_argument("trailing characters");
        }
        return value;
    } catch (const std::exception&) {
        throw std::runtime_error("invalid integer: " + text);
    }
}

std::uint32_t parse_seed(const std::string& text) {
    try {
        std::size_t consumed = 0;
        const unsigned long long value = std::stoull(text, &consumed);
        if (consumed != text.size()) {
            throw std::invalid_argument("trailing characters");
        }
        return static_cast<std::uint32_t>(value);
    } catch (const std::exception&) {
        throw std::runtime_error("invalid seed: " + text);
    }
}

void print_stats(const std::string& label, const Stats& stats, double theory_mean,
                 double theory_sd) {
    std::cout << label << ": n=" << stats.n << "\n";
    std::cout << "  mean=" << std::fixed << std::setprecision(1) << stats.mean
              << "  sd=" << stats.sd << "\n";
    std::cout << "  min=" << stats.min << " max=" << stats.max << "\n";
    std::cout << "  theoretical_mean=" << std::fixed << std::setprecision(1)
              << theory_mean << " theoretical_sd=" << theory_sd << "\n";
}

}  // namespace

int main(int argc, char** argv) {
    Options options;
    try {
        for (int i = 1; i < argc; ++i) {
            const std::string arg = argv[i];
            auto value = [&](const std::string& name) -> std::string {
                if (i + 1 >= argc) {
                    throw std::runtime_error("missing value for " + name);
                }
                return argv[++i];
            };

            if (arg == "--self-test") {
                options.self_test = true;
            } else if (arg == "--arm") {
                options.arm = value(arg);
            } else if (arg == "--target") {
                options.c = parse_int(value(arg));
                options.d = parse_int(value(arg));
            } else if (arg == "--trials") {
                const std::string raw = value(arg);
                try {
                    options.trials = std::stoll(raw);
                } catch (const std::exception&) {
                    throw std::runtime_error("invalid --trials: " + raw);
                }
            } else if (arg == "--seed") {
                options.seed = parse_seed(value(arg));
            } else if (arg == "--lo") {
                options.lo = parse_int(value(arg));
            } else if (arg == "--hi") {
                options.hi = parse_int(value(arg));
            } else if (arg == "--out") {
                options.out = value(arg);
            } else if (arg == "--help" || arg == "-h") {
                print_usage();
                return 0;
            } else {
                throw std::runtime_error("unknown argument: " + arg);
            }
        }
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << "\n";
        print_usage();
        return 2;
    }

    if (options.self_test) {
        return self_test() ? 0 : 1;
    }

    if (options.arm != "control" && options.arm != "select" && options.arm != "both") {
        std::cerr << "error: --arm must be control, select or both\n";
        return 2;
    }
    if (options.trials < 1) {
        std::cerr << "error: --trials must be >= 1\n";
        return 2;
    }
    if (options.lo > options.hi) {
        std::cerr << "error: --lo must be <= --hi\n";
        return 2;
    }
    if (options.c < options.lo || options.c > options.hi || options.d < options.lo ||
        options.d > options.hi) {
        std::cerr << "error: --target values must lie inside [--lo, --hi]\n";
        return 2;
    }

    std::ofstream csv;
    if (!options.out.empty()) {
        csv.open(options.out);
        if (!csv) {
            std::cerr << "error: cannot open --out file: " << options.out << "\n";
            return 2;
        }
        csv << "trial,seed,target_c,target_d,arm,iterations,final_x,final_y\n";
    }

    std::vector<long long> control_values;
    std::vector<long long> select_values;
    long long mismatches = 0;

    for (long long trial = 0; trial < options.trials; ++trial) {
        const std::uint32_t seed =
            options.seed + static_cast<std::uint32_t>(trial);

        if (options.arm == "control" || options.arm == "both") {
            const TrialResult result =
                run_trial(false, seed, options.c, options.d, options.lo, options.hi);
            control_values.push_back(result.iterations);
            if (csv) {
                csv << trial << ',' << seed << ',' << options.c << ',' << options.d
                    << ",control," << result.iterations << ',' << result.final_x << ','
                    << result.final_y << '\n';
            }
        }
        if (options.arm == "select" || options.arm == "both") {
            const TrialResult result =
                run_trial(true, seed, options.c, options.d, options.lo, options.hi);
            select_values.push_back(result.iterations);
            if (csv) {
                csv << trial << ',' << seed << ',' << options.c << ',' << options.d
                    << ",select," << result.iterations << ',' << result.final_x << ','
                    << result.final_y << '\n';
            }
        }
        if (options.arm == "both" &&
            control_values.back() != select_values.back()) {
            ++mismatches;
        }
    }

    const double probability =
        target_prob(options.c, options.d, options.lo, options.hi);
    const double theory_mean = 1.0 / probability;
    const double theory_sd = std::sqrt((1.0 - probability) / (probability * probability));

    std::cout << "mode=" << (options.arm == "both" ? "paired" : "single")
              << " arm=" << options.arm << " target=(" << options.c << ","
              << options.d << ") trials=" << options.trials << " lo=" << options.lo
              << " hi=" << options.hi << " seed0=" << options.seed << "\n";
    if (options.arm == "both") {
        std::cout << "mismatches=" << mismatches << "\n";
        print_stats("control", summarize(control_values), theory_mean, theory_sd);
        print_stats("select", summarize(select_values), theory_mean, theory_sd);
    } else if (options.arm == "control") {
        print_stats("control", summarize(control_values), theory_mean, theory_sd);
    } else {
        print_stats("select", summarize(select_values), theory_mean, theory_sd);
    }

    return 0;
}
