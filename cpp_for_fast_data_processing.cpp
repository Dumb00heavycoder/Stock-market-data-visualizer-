// C++ code: moving_average.cpp
#include <vector>

std::vector<double> moving_average(const std::vector<double>& data, int window) {
    std::vector<double> result(data.size());
    double sum = 0.0;
    for (size_t i = 0; i < data.size(); ++i) {
        sum += data[i];
        if (i >= window) sum -= data[i - window];
        if (i >= window - 1) result[i] = sum / window;
    }
    return result;
}
