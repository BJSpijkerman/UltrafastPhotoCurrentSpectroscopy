#ifndef PROGRESSBAR_HPP
#define PROGRESSBAR_HPP

#include "indicator.hpp"

#include <mutex>
#include <algorithm>
#include <string>

class ProgressBar : public IIndicator {
public:
    void set_progress(float value) {
        std::unique_lock lock{mutex_};
        progress_ = std::clamp(value, 0.0f, 100.0f);
    }

    void set_bar_width(std::size_t width) {
        std::unique_lock lock{mutex_};
        bar_width_ = width;
    }

    void set_fill_bar_progress_with(const std::string& chars) {
        std::unique_lock lock{mutex_};
        fill_ = chars;
    }

    void set_fill_bar_remainder_with(const std::string& chars) {
        std::unique_lock lock{mutex_};
        remainder_ = chars;
    }

    void set_status_text(const std::string& status) {
        std::unique_lock lock{mutex_};
        status_text_ = status;
    }

    void update(float value) {
        set_progress(value);
    }

    // IIndicator
    void write_progress(std::ostream& os) override {
        std::unique_lock lock{mutex_};

        os << "\r[";

        const std::size_t completed =
        static_cast<std::size_t>(progress_ * (float)bar_width_ / 100.0f);

        for (std::size_t i = 0; i < bar_width_; ++i) {
            os << (i < completed ? fill_ : remainder_);
        }

        os << "] "
        << static_cast<std::size_t>(progress_) << "% "
        << status_text_ << std::flush;
    }

    // Clean progress bar
    void end_bar(std::ostream& os) {
	set_progress(100.0f);
	os << std::endl;
    }

private:
    std::mutex mutex_;
    float progress_{0.0f};
    std::size_t bar_width_{60};
    std::string fill_{"#"};
    std::string remainder_{" "};
    std::string status_text_{""};
};

#endif
