#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#include <queue>
#include <thread>
#include <vector>
#include <mutex>
#include <functional>
#include <condition_variable>
#include <chrono>
#include <future>

using namespace std;

namespace ThreadPool{
    class ThreadPool{
    public:
        ThreadPool(size_t num_threads);
        ~ThreadPool();
        
        
        // Job을 추가
        template <class F, class... Args>
        future<typename result_of<F(Args...)>::type> enqueueJob(F&& f, Args&&... args);
        
        void end();
        
    private:
        size_t num_threads;
        vector<thread> worker_threads;
        queue<function<void()>> jobs;
        int cur_working;
        
        condition_variable cv_job_q;
        mutex mutex_job_q;

        
        bool stop_all;
        
        void workerThread();
    };

    ThreadPool::ThreadPool(size_t num_threads) : num_threads(num_threads), stop_all(false), cur_working(0){
        worker_threads.reserve(num_threads);
        for(size_t i = 0; i < num_threads; i++){
            worker_threads.emplace_back([this]() { this->workerThread(); });
        }
    }

    void ThreadPool::workerThread(){
        while(true){
            // 큐에 접근하여 job을 빼내는 과정을 mutex_job_q로 관리
            unique_lock<mutex> lock(mutex_job_q);
            // condition_variable에 wait을 호출해서 lock을 내려놓고, 깨울때까지 대기 
            cv_job_q.wait(lock, [this]() { return !this->jobs.empty() || (stop_all && cur_working == 0); });
            if (stop_all && this->jobs.empty()){
                cv_job_q.notify_all();
                return;
            }
            
            // 가장 앞의 job을 뺀다.
            function<void()> job = move(jobs.front());
            jobs.pop();
            cur_working++;
            lock.unlock();
            
            // 해당 job을 수행한다.
            job();
            
            lock.lock();
            cur_working--;
        }
    }

    ThreadPool::~ThreadPool(){
        if (!stop_all){
            end();
        }
    }

    template <class F, class... Args>
    future<typename result_of<F(Args...)>::type> ThreadPool::enqueueJob(F&& f, Args&&... args){
        
        using return_type = typename result_of<F(Args...)>::type;    
        auto job = make_shared<packaged_task<return_type()>>(bind(forward<F>(f), forward<Args>(args)...));
        
        future<return_type> job_result_future = job->get_future();
        {
            // lock guard를 써서 해당 블록을 벗어날 때 알아서 unlock됨
            lock_guard<mutex> lock(mutex_job_q);
            jobs.push([job]() { (*job)(); });
        }
        cv_job_q.notify_one();
        
        return job_result_future;
    }
    
    void ThreadPool::end(){
        stop_all = true;
        cv_job_q.notify_all();
        
        for(auto& t : worker_threads){
            t.join();
        }
    }
}

#endif
