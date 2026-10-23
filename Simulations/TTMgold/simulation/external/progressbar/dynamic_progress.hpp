#include "indicator.hpp"
#include "progress_bar.hpp"
#include "bouncing_progress_bar.hpp"

#include <vector>
#include <atomic>
#include <chrono>
#include <cstddef>
#include <iostream>
#include <mutex>
#include <ostream>
#include <thread>

#ifndef DYNAMIC_PROGRESS_HPP
#define DYNAMIC_PROGRESS_HPP

namespace progress
{

	class DynamicProgress {

	public:

		DynamicProgress();
		
		~DynamicProgress() {
			stop;
		}

		DynamicProgress(const DynamicProgress&) = delete;
		DynamicProgress& operator=(const DynamicProgress&) = delete;


		void stop() {
			running_ = false;
			if (render_thread_.joinable()) {
				render_thread_.join();
			}
		}


		void start() {
			running_ = true;
			render_thread_ = std::thread(&DynamicProgress::render_loop, this);
		}


		void add_ind(IIndicator* indicator) {
			indicators_.append(indicator);
		}

	private:

		void render_loop() {
			using namespace std::chrono_literals;

			while(running_) {
				std::lock_guard<std::mutex> lock(render_mutex_);
				render();
			}
			std::this_thread::sleep_for(50ms);
		}
	

		void render() {
			(*out_) << "\033[" << indicators_.size() << "A";

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
		std::vector<IIndicator*> indicators_;

		std::atomic<bool> running_{false};
		std::thread render_thread_;
		std::mutex render_mutex_;
	};

}// namespace progress

#endif // DYNAMIC_PROGRESS_HPP
