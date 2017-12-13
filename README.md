# newseed.cn-spider
By selenium, crawl all the information about investments available on http://www.newseed.cn/invest <br />

All infomation in the highlighted box are crawled, for all the events available. <br />
[Information to be crawled](pics/input1.png) <br />
[Detailed information to be crawled](pics/input2.png) <br />

The output is saved into a single .csv file. <br />
[The output looks like this](pics/output.png) <br />
The extra columns and redundant column names are generated during batch processing and can be easily removed afterwards. <br />

Running environment: <br />
python-2.7.12, ubuntu-16.04-LTS, latest Firefox (with geckodriver executable) <br />

Configure: <br />
Please first execute config.sh to ensure all packages required are installed. <br />

Column name keys: <br />
date: 投资时间 <br />
financier: 受资方 <br />
industry: 所属领域 <br />
investors: 投资方 <br />
quantity: 融资金额 <br />
rounds: 轮次 <br />
title: 融资事件 <br />
