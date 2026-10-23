#ifndef BOUNCING_PROGRESSBAR_HPP
#define BOUNCING_PROGRESSBAR_HPP

#include "indicator.hpp"

#include <mutex>
#include <string>
#include <algorithm>

class BouncingProgressBar : public IIndicator {
public:
    void start() {
        std::unique_lock lock{mutex_};
        running_ = true;
    }

    void stop() {
        std::unique_lock lock{mutex_};
        running_ = false;
    }

    void tick() {
        std::unique_lock lock{mutex_};

        if (!running_ || bar_width_ <= block_width_)
            return;

        auto now = std::chrono::steady_clock::now();
        if (now - last_update_ < update_interval_)
            return; // skip this tick to debounce

            last_update_ = now;

        position_ += direction_;

        if (position_ == 0 ||
            position_ + block_width_ >= bar_width_) {
            direction_ = -direction_;
            }
    }

    void set_bar_width(std::size_t width) {
        std::unique_lock lock{mutex_};
        bar_width_ = width;
        position_ = std::min(position_, bar_width_);
    }

    void set_block(const std::string& block) {
        std::unique_lock lock{mutex_};
        block_ = block;
        block_width_ = block_.size();
    }

    void set_remainder(const std::string& chars) {
        std::unique_lock lock{mutex_};
        remainder_ = chars;
    }

    void set_status_text(const std::string& status) {
        std::unique_lock lock{mutex_};
        status_text_ = status;
    }

    // IIndicator
    void write_progress(std::ostream& os) override {
        std::unique_lock lock{mutex_};

        os << "\r[";

        for (std::size_t i = 0; i < bar_width_; ++i) {
            if (i == position_) {
                os << block_;
                i += block_width_ - 1;
            } else {
                os << remainder_;
            }
        }

        os << "] " << status_text_;
    }

private:
    std::mutex mutex_;

    std::chrono::steady_clock::time_point last_update_{};
    std::chrono::milliseconds update_interval_{100}; // 100 ms per step

    std::size_t bar_width_{60};
    std::size_t position_{0};
    int direction_{1};
    bool running_{false};

    std::string block_{"<=>"};
    std::size_t block_width_{3};

    std::string remainder_{" "};
    std::string status_text_{"working..."};
};

#endif
