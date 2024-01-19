# CASE STUDY 2
There are two things I want to highlight for mass data scraping according to the 1st case: **Parallel Processing** and **Exception Handling**.

## Parallel Processing

Scraping data is time-consuming, it involves simulating browser, user interaction, content loading, etc. It's a time-consuming process, and is such an enemy for every project. 

In the 1st case, I made the program run sequentially, which took longer as processes waited for each other. While some processes indeed require waiting, but others can run independently. Utilizing parallel processing allows these independent processes to run concurrently, cutting the runtime and accelerating result.

**asynchronous process**

Based on the 1st case, notice that every time the program moves to the other search page of Tokopedia, the parameter of the endpoint changes from, for example, `/search?q=rockbros&page=1` to `/search?q=rockbros&page=2` and so on. That means, there's no need to click the navigation button to navigate the page. We just need to visit the endpoint, passing the `page` parameter as desired and scrape the data.

Utilizing Playwright's async ability with Asyncio, we can generate 10 endpoints with `page` parameter from 1 to 10, assign them to the workers and run concurrently as the main program wait for them to finish. This is just one method that can be applied.

**pandas is notoriously slow**

in my experience with pandas, one way to improve its performance is to use the right method for the right purpose. Two or more methods in pandas could have the same purpose but different performance. For instance, the method `str.replace()` in the 1st case has the same purpose as method `replace()` but give a different performance where the `str.replace()` method gives faster runtime execution.

The problem with pandas is that it’s not async-friendly. It doesn’t support Asyncio. However, we can still utilize other library, such as Celery to deploy a distributed task queue.

## Exception Handling

I encountered some exceptions when I was writing the code. One of the exceptions that raised the most was `TimeoutException` from Playwright. The exception raised when the Locator failed to find the page element. Some factors that cause the `Locator` to fail were because the element didn’t exist, failed to load, or changed.

**custom exception**

Custom Exceptions would be beneficial for developers in this case. Creating custom exceptions that unique to some cases helps developers understand the error. A clear error message, error code, and error log make the debugging process faster.

**early warning system (ews)**

To reduce the possibility of raising Exceptions, it's crucial to implement an Early Warning System just before initiating the scraping process. An example of an EWS involves verifying the validity of all required web resources. At least three questions that need to be answered by this ews regarding data scraping: Does the element exist? Is the element valid? Does the element contain the expected data? When all of the answers to the questions are true, then scrapping can be started. Otherwise, some investigations are needed.