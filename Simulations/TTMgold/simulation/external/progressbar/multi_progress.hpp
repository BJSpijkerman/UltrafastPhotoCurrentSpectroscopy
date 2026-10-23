#ifndef MULTIPROGRESS_HPP
#define MULTIPROGRESS_HPP

#include "indicator.hpp"
#include "progress_bar.hpp"
#include "bouncing_progress_bar.hpp"

#include <array>
#include <atomic>
#include <chrono>
#include <cstddef>
#include <iostream>
#include <mutex>
#include <ostream>
#include <thread>

namespace progress
{

    template<std::size_t Count>
    class MultiProgress
    {
    public:
        /// Construct with exactly Count indicators, output defaults to std::cout
        template<typename... Indicators>
        explicit MultiProgress(std::ostream& out = std::cout,
                               Indicators&... indicators)
        : out_(&out)
        , indicators_{ static_cast<IIndicator*>(&indicators)... }
        {
            static_assert(sizeof...(Indicators) == Count,
                          "Number of indicators must match Count");

            start();
        }

        // Non-copyable (owns a thread)
        MultiProgress(const MultiProgress&) = delete;
        MultiProgress& operator=(const MultiProgress&) = delete;

        ~MultiProgress()
        {
            stop();
        }

        void stop()
        {
            running_ = false;
            if (render_thread_.joinable()) {
                render_thread_.join();
            }
        }

    private:
        void start()
        {
            running_ = true;
            render_thread_ = std::thread(&MultiProgress::render_loop, this);
        }

        void render_loop()
        {
            using namespace std::chrono_literals;

            while (running_) {
                {
                    std::lock_guard<std::mutex> lock(render_mutex_);
                    render();
                }
                std::this_thread::sleep_for(50ms);
            }
        }

        void render()
        {
            (*out_) << "\033[" << Count << "A";

            for (auto* ind : indicators_) {
                (*out_) << "\33[2K\r";
                //ind->render(*out_);
                ind->write_progress(*out_);
                (*out_) << '\n';
            }

            out_->flush();
        }

    private:
        std::ostream* out_;
        std::array<IIndicator*, Count> indicators_;

        std::atomic<bool> running_{false};
        std::thread render_thread_;
        std::mutex render_mutex_;
    };

} // namespace progress

#endif // MULTIPROGRESS_HPP
