# Cluster evaluation

## Tested Methods

affinity_propagation
birch
hdbscan
hdbscan_lda
meanshift
spectral_clustering

## Scores

Normalized mutual information
Completeness score

## Results

### Best score per method

SELECT method, MAX(normalized_mutual_info_score) as nmi,MAX(completeness_score) as completeness FROM `method_evaluation` group by method order by nmi desc

method	nmi   	completeness	
affinity_propagation	0.740863	0.50566	
hdbscan	                0.733162	0.680484	
birch	                0.639539	0.137502	
spectral_clustering	    0.554214	0.43573	
hdbscan_lda	            0.509255	0.425517	
meanshift	            0.33316 	0.058969

#### Context 

SELECT * FROM `method_evaluation` as m WHERE `normalized_mutual_info_score` = (SELECT Max(`normalized_mutual_info_score`) FROM `method_evaluation` m2 where m.method = m2.method) order by normalized_mutual_info_score desc

### Number of estimated clusters vs real

SELECT method, Min(Abs(real_clusters - estimated_clusters)) as difference FROM `method_evaluation` group by method order by difference ASC


method	difference   	
hdbscan	                0	
hdbscan_lda	            1	
affinity_propagation	7	
spectral_clustering	    8	
meanshift	            15	
birch	                451	

#### Context

SELECT * FROM `method_evaluation` as m WHERE Abs(real_clusters - estimated_clusters) = (SELECT Min(Abs(real_clusters - estimated_clusters)) FROM `method_evaluation` m2 where m.method = m2.method)

### Average processing time 

SELECT method, AVG(processing_time) as average_processing_time FROM `method_evaluation` where sample_size = 2000 group by method order by average_processing_time ASC


method	average_processing_time   	
hdbscan	0.29650445949907106	
birch	1.2744041537797008	
affinity_propagation	14.408452648669481	
hdbscan_lda	154.53434733549753	
meanshift	440.7399781545003	
spectral_clustering	461.2059956267476	

## Analyze clusters

### Find news belonging to clusters from a certain evaluation

SELECT n.title, c.id, n.story FROM news_article as n
Join cluster_news_article as cn on cn.news_article_id = n.id
Join cluster as c on c.id = cn.cluster_id
Where c.method_evaluation_id = 1584
order by n.story

### Number of clusters per story (should be 1:1)
SELECT n.story, count(DISTINCT c.id) as nclusters FROM news_article as n
Join cluster_news_article as cn on cn.news_article_id = n.id
Join cluster as c on c.id = cn.cluster_id
Where c.method_evaluation_id = 1584
group by n.story
order by n.story

### Find news articles classified as noise

-- This query can take a couple of minutes.

SELECT * from news_article as nn where nn.story in (
	SELECT n.story FROM news_article as n
	Join cluster_news_article as cn on cn.news_article_id = n.id
	Join cluster as c on c.id = cn.cluster_id
	Where c.method_evaluation_id = 1610 
	group by n.story )
and not exists (
	SELECT c.id FROM cluster_news_article as cna
	Join cluster as c on c.id = cna.cluster_id
	Where c.method_evaluation_id = 1610 and cna.news_article_id = nn.id
)
and newspaper_processed = 1
AND title_keywords_intersection = 1
AND hostname != 'newsledge.com'
AND hostname != 'www.newsledge.com'
AND newspaper_text IS NOT NULL
AND TRIM(COALESCE(newspaper_text, '')) != ''
AND newspaper_text NOT LIKE '%%GDPR%%'
AND newspaper_text NOT LIKE '%%javascript%%'
AND newspaper_text NOT LIKE '%%404%%'
     


50874	Leading auto finance company Ally Financial sets terms for $2.5 billion IPO	http://www.nasdaq.com/article/leading-auto-finance-company-ally-financial-sets-terms-for-25-billion-ipo-cm339269	NASDAQ	b	d_iR-3SNitL0XpMhHYUo-DTelAK1M	www.nasdaq.com	2014-03-27 20:14:40	1		en	auto,x,target,setting,company,gray,ally,settings,change,selection,sets,leading,financial,ipo,billion,symbols,close,default,finance,terms	"CLOSE X Edit Favorites Enter up to 25 symbols separated by commas or spaces in the text box below. These symbols will be available during your session for use on applicable pages. Update

Clear List CLOSE X Customize your NASDAQ.com experience Background Color Selector

Select the background color of your choice: Black Slate Gray Light Gray Gray Blue

Quote Search

Select a default target page for your quote search: Real-Time

After Hours

Pre-Market

News Flash Quote

Summary Quote

Interactive Charts

Default Setting





If you have any questions or encounter any issues in changing your default settings, please email Please note that once you make your selection, it will apply to all future visits to NASDAQ.com. If, at any time, you are interested in reverting to our default settings, please select Default Setting above.If you have any questions or encounter any issues in changing your default settings, please email isfeedback@nasdaq.com CLOSE X Please confirm your selection: You have selected to change your default setting for the Quote Search. This will now be your default target page; unless you change your configuration again, or you delete your cookies. Are you sure you want to change your settings? YES NO"																					1	0	0
50891	Fed Approves Ally's Capital Plan In Milestone for Potential IPO	http://blogs.wsj.com/moneybeat/2014/03/26/fed-approves-allys-capital-plan-in-milestone-for-potential-ipo/	Wall Street Journal \(blog\)	b	d_iR-3SNitL0XpMhHYUo-DTelAK1M	blogs.wsj.com	2014-03-27 20:14:45	1		en	bank,capital,approved,financial,ipo,potential,regulators,reserve,allys,federal,severe,report,plan,approves,fed,review,milestone	"The Federal Reserve approved Ally Financial Inc.’s capital plan in the bank regulator’s annual review of the industry’s financial health, clearing another potential hurdle to the auto lender’s plans to exit government ownership.

Ally’s plan was approved after the Federal Reserve found that the bank could keep lending in a severe economic downturn, according to a report Wednesday."																					1	0	1
56720	Here's what's trending: New leads on MH370; Obamacare enrollment hits 6  ...	http://blog.al.com/wire/2014/03/heres_whats_trending_new_leads.html	al.com \(blog\)	b	d_hW9mavhlXZ9mMP2sSzq7LOou5ZM	blog.al.com	2014-03-28 14:16:03	1		en	hits,report,law,leads,christie,visa,suit,walmart,million,released,whats,associated,mh370,trending,support,obamacare,sues,documents,world	"There's no need to ever feel left out again at the water cooler conversation. Here's a rundown of the stories currently trending in the world, the country and your backyard.

Yahoo





New lead: The focus of the search for missing Malaysian Airlines Flight 370 shifted Friday on news of a “new credible lead" about the planes last known position. Searchers are now looking for the plane in an area nearly 700 miles northeast of where efforts had been centered. Full story: The Associated Press



Numbers up, support down: The White House announced Thursday that 6 million people have signed up for health insurance under the Affordable Care Act. The deadline to sign up before being hit with a penalty is Monday. The results of an Associated Press poll released Thursday revealed that public support for the law is at its lowest level ever. Twenty-six percent of those surveyed support the law. Full story: Politico



Christie report: A law firm hired by New Jersey Gov. Chris Christie has released a report that says that Christie did not order the closing of lanes of the George Washington Bridge in September 2013, and had no knowledge of the plan before or immediately after the fact. The report concluded that David Wildstein, a longtime Christie associate, and Bridget Anne Kelly, Christie’s deputy chief of staff at the time, were behind the lane closings in an act of political revenge against the mayor of Fort Lee. Full story: The Associated Press



Google

More documents to be released: The National Archives on Friday will release another 2,500 pages of documents from President Bill Clinton’s time in the White House. The documents are expected to include the president’s farewell address and records from aides. Full story: The Associated Press



Walmart sues Visa: Walmart has filed suit against Visa, saying the credit card company conspired with banks to fix fees that retailers pay for accepting the credit card. The suit seeks more than $5 billion. The suit also says the magnetic strips on Visa cards are “inherently insecure.” Full story: Bloomberg

Click here for more world and national news



YouTube



Are the squirrels up north really that friendly? Wouldn’t want to bet my finger on it. Love the hat, though.

She’s cookin’ on all kinds of levels. The dog looks like he’s seen it before.

Follow Debbie Lord on Twitter at Follow @DebbieMLord







"																					1	0	1
56725	Walmart suing credit card company over fees it charges when customers use  ...	http://www.krmg.com/news/news/local/walmart-suing-credit-card-company-over-fees-it-cha/nfMx2/	KRMG	b	d_hW9mavhlXZ9mMP2sSzq7LOou5ZM	www.krmg.com	2014-03-28 14:16:04	1		en	suing,findings,company,trump,special,russian,campaign,credit,charges,card,custo,walmart,fees,president,rep,congress,mueller,counsel	Armed with his Attorney General's summary of a lengthy report by Special Counsel Robert Mueller into Russian interference in the 2016 elections, President Donald Trump was up early on Monday morning celebrating the findings of that probe, joining GOP lawmakers in Congress in declaring that his campaign had been cleared of any questions of wrongdoing. 'The Special Counsel did not find that the Trump Campaign, or anyone associated with it, conspired or coordinated with the Russian Government in these efforts, despite multiple offers from Russian-affiliated individuals to assist the Trump Campaign,' the President tweeted early on Monday, quoting from a letter sent Sunday by Attorney General William Barr to Congress. The four page letter from Barr - summarizing the findings of the Mueller investigation - found no conspiracy existed between the Trump campaign and Russia during the 2016 election, even as Russian intelligence hacked Democratic Party emails, and 'despite multiple. offers from Russian-affiliated individuals to assist the Trump campaign.' 'But as noted above, the Special Counsel did not find that the Trump campaign, or anyone associated with it, conspired or coordinated with the Russian government in these efforts,' the letter from Barr noted. In Congress, Republican lawmakers gleefully joined the President in heralding the findings, trying their best to undercut any ongoing efforts by Democrats to further dig into the details of the Mueller report - which the Attorney General said he would strive to make as much public as possible in the weeks and months ahead. 'There was NO collusion between Russia and President Donald Trump or his campaign,' said Rep. Tom Cole (R-OK). 'Facts trump the liberal circus, every time,' said Rep. Doug Collins (R-GA). 'Democrats in Congress should follow his lead and allow the President to govern as he was elected by the American people to do,' said Rep. Neal Dunn (R-FL). 'After two years the case is closed.' As for Democrats, they quickly dug into the details of the Barr letter and focused on getting the details of the Mueller report made public, zeroing in on Barr's description that Mueller had made no conclusions about whether President Trump had obstructed during the Russia investigation. 'The Special Counsel states that 'while this report does not conclude that the President committed a crime, it also does not exonerate him,'' Barr quoted the Mueller findings. 'There must be full transparency in what Special Counsel Mueller uncovered to not exonerate the President from wrongdoing,' said Rep. Jerry Nadler (D-NY), the head of the House Judiciary Committee, who vowed to press for more documents and hearings about the Mueller investigation. 'Questions remain related to evidence of obstruction of the investigation into Russian election interference,' said Rep. Ted Deutch (D-FL). The findings - as related by the Attorney General on Sunday - clearly made any chance of impeachment proceedings against the President in Congress much less of a possibility, both easing the political pressure on Mr. Trump, and at the same time giving him a public boost which his campaign quickly jumped on for supporters. The President was already scheduled to take his message on the road for a campaign rally on Thursday in Michigan.																					1	0	1
56753	Market Update: Visa Inc (NYSE:V) – Wal-Mart sues Visa for $5 billion over card  ...	http://jutiagroup.com/20140327-market-update-visa-inc-nysev-wal-mart-sues-visa-for-5-billion-over-card-swipe-fees/	Jutia Group	b	d_hW9mavhlXZ9mMP2sSzq7LOou5ZM	jutiagroup.com	2014-03-28 14:16:11	1		en	value,analysis,zngtsxv,stock,investment,good,sees,zinc,technical,maund,sure,market,resources	Technical analyst Clive Maund explains why he sees this zinc explorer as a good value. To be sure, Group Eleven Resources Corp.’s (ZNG:TSX.V; GRLVF:OTCQB) stock looks cheap here and good value. It is an advanced […]																					1	0	1
68186	There's much to be said for normality in the US economy	http://www.independent.co.uk/voices/commentators/theres-much-to-be-said-for-normality-in-the-us-economy-9223569.html	The Independent	b	d_gVpCAKL5OJx5MwfYTkwNfgtpTYM	www.independent.co.uk	2014-03-31 03:54:24	1		en	normal,rates,economy,theres,world,swings,growth,fed,developed,boom,yellen,normality	"There is a spring in the step of the US economy, and it has to do not just with the better data coming through, but with a wider sense that the country is returning to “normal”. That is, normal interest rates, normal growth and normal levels of unemployment.

You have to be cautious when trying to pin down anything so nebulous as economic sentiment, but one recent shift is significant. It concerns the assurance that Janet Yellen, the new chair of the Federal Reserve Board, has given people that the Fed will, so to speak, do the right thing. She gave her first press conference here in Washington nearly two weeks ago, noting that interest rates would stay low for a considerable period after the Fed stopped its monthly purchase of treasury debt. When asked how long this might be, she said it might be “around six months or that type of thing”.

The initial reaction of one of shock – gosh, that means rates will start to go up about March next year rather than six months later as previously expected – and markets plunged. But since then there has been a reassessment. People have looked at the totality of what she said together with the Fed’s opening statement, instead of picking on one remark. Taken overall, this is that the Fed would continue with an exceptionally loose monetary policy for a while yet, but eventually policy would return to normal. The pace would be determined by the pace of the economy, and not triggered by a specific number such as the unemployment rate.

We’ll tell you what’s true. You can form your own view. From 15p €0.18 $0.18 USD 0.27 a day, more exclusives, analysis and extras.

Put that way, what the Fed was seeking to do looked rather sensible – and, consequently, Ms Yellen appears rather sensible too. The return to normal interest rates is seen more as a signal that the economy is indeed back to normal than something to be feared.

But what is normal? The years up to the global financial crisis have come to be dubbed the “great moderation”. The developed world had periods of boom and bust but the magnitude of the swings seemed to be decreasing. Gordon Brown took some stick for claiming that Labour had eliminated “Tory boom and bust”, but if you take out the politics, his hubris mirrored that of the bankers who assumed that big swings in the economy would not occur again. We know now how wrong both were, and most of us assume that there will be big swings in the economy, here in the US as well as elsewhere, in the future. The new normal, it is widely argued, will be different from the old normal.

That may turn out to be right, but people in the US are beginning to wonder whether another period of the great moderation may have already begun. The most developed version of this argument has just been produced by the global economics team at Goldman Sachs. Their argument is that between 1984 and 2007, volatility fell in most of the developed world. It certainly happened in the US, but it also occurred in the UK. The early 1990s recession was not as bad as the early 1980s one, and the early 2000s downturn was not technically a recession at all. Then everyone became complacent and made huge errors of judgement, with the results we all know.

Now, the Goldman team argues, stability has returned. The data for the past three years shows that US employment has grown more steadily than at any time for the past 50 years. Consumption in the US had grown equally steadily. If this is right, the US will have several years of steady growth. One of the effects of tightened regulation in the banking sector will be to restrict the extent to which companies and households increase their borrowings. So the dangers of a boom getting out of control are much less. On the other side, we are less likely to plunge into a slump because the authorities have shown they will act to check that. After all, that is what the Fed has done and is committed to continuing. Janet Yellen made that quite clear.

I find this argument quite convincing. There has been much concern on both sides of the Atlantic about the quality of the recovery: that it is weaker than that of previous cycles and that it has been sustained only by the artificial stimulus of QE, which brings other problems. Those are reasonable worries and will continue until such time as living standards have recovered to their previous levels. There is a further concern. Lower volatility – not so high booms and not so deep slumps – does not of itself mean faster long-term growth. It may make it easier to sustain solid growth, and socially it is highly desirable. Not many people think boom and bust is a great way to run things.

Nevertheless, an America that grows steadily for the next four years would become a locomotive for the rest of the developed world. Goldman forecasts growth at or about 3 per cent through to the end of 2017 for both the US and UK. If that turns out to be the new normal, normal sounds OK to me.

We’ll tell you what’s true. You can form your own view.

At The Independent, no one tells us what to write. That’s why, in an era of political lies and Brexit bias, more readers are turning to an independent source. Subscribe from just 15p a day for extra exclusives, events and ebooks – all with no ads.

Subscribe now"																					1	0	1
68187	Chair of the Federal Reserve: Who is Janet Yellen?	http://www.allgov.com/news/appointments-and-resignations/chair-of-the-federal-reserve-who-is-janet-yellen-140329\?news=852790	AllGov	b	d_gVpCAKL5OJx5MwfYTkwNfgtpTYM	www.allgov.com	2014-03-31 03:54:24	1			economics,summers,federal,economic,post,reserve,janet,chair,university,fed,yellen,berkeley,yellens	"On February 3, 2014, Janet Yellen was sworn in as chair of the Federal Reserve. In taking over from Ben Bernanke, Yellen became the first woman to lead the institution that controls much of the financial system of the United States. She was nominated to the post on October 9, 2013 by President Barack Obama.

Yellen was born August 13, 1946, in Brooklyn, New York. She graduated from Fort Hamilton High School in Brooklyn and went on to attend Brown University. She received a B.A. in economics from that school in 1967. Yellen then moved to Yale University, from which she earned a Ph.D. in economics in 1971.

She became an assistant professor at Harvard, and taught there from 1971 to 1976. While at Harvard, one of her students was Lawrence Summers, who later became Secretary of the Treasury under President Bill Clinton and director of the National Economic Council under Obama.

Yellen then moved to a job at the Fed, becoming an economist in its division of international finance. While there, she met fellow economist George Akerlof, whom she married. Akerlof went on to win the 2001 Nobel Prize in economics, sharing it with A. Michael Spence and Joseph Stiglitz. Stiglitz was one of Yellen’s teachers at Yale.

In 1978, Yellen moved to Great Britain, teaching at the London School of Economics. She returned to the United States in 1980, accepting a post at the University of California Berkeley. Berkeley became her academic home from then on, taking leaves to accept government posts, but returning to the university when out of government. One of Yellen’s major works at Berkeley was co-authorship of a study dealing with East Germany’s integration into the German economy upon the reunification of the country. In 1993 Yellen endorsed the North American Free Trade Agreement (NAFTA).

Yellen took a leave from Berkeley in 1994, serving on the Federal Reserve System’s board of governors until 1997. At the time, her nomination was criticized by some because of Yellen’s lack of commercial banking experience. Then, Clinton appointed Yellen as chair of his Council of Economic Advisors, succeeding her old teacher Stiglitz. She served there until 1999, when she returned to California.

In 2004, Yellen was made president of the Federal Reserve Bank in San Francisco. She was one of the first to herald the coming financial crisis in 2007, urging tightening of rules for making home loans. She later acknowledged, however, that the San Francisco Fed didn’t do all it could have to ameliorate the crash, particularly in respect to Countrywide Financial’s toxic loan portfolio.

Yellen left San Francisco in 2010, when Obama nominated her to be vice chair of the Fed. She was sworn into that post in October of that year. There, she urged the Fed to maintain ultra-low interest rates and to continue bond purchases that would help spur economic growth during the slow recovery.

When Bernanke announced his departure as Fed chair, Yellen’s former student Summers was seen as a front-runner to fill the post. However, questions about Summers’ temperament persisted, and Summers withdrew from consideration and Obama nominated Yellen to the post.

Yellen and Akerlof have a son, Robert Akerlof, who has followed in his parents’ footsteps. He is an economist who teaches at the University of Warwick in Coventry, England. Yellen’s passions include stamp collecting and going on holiday with stacks of economic books for summer reading.

-Steve Straehley

To Learn More:

Janet Yellen: An Updated Reading List (by Sarah Wheaton, New York Times)

Janet Yellen Urged Glass-Steagall Repeal And Social Security Cuts, Supported NAFTA (by Zach Carter, Huffington Post)

Fed Chair Candidate Could Bring Brown to D.C. (by Brittany Nieves, Brown Daily Herald)"																					1	0	1
68188	Gold Prices to Continue Exhibiting Weakness	http://www.ibtimes.co.uk/gold-prices-continue-exhibiting-weakness-1442439	International Business Times UK	b	d_gVpCAKL5OJx5MwfYTkwNfgtpTYM	www.ibtimes.co.uk	2014-03-31 03:54:24	1		en	price,weakness,week,weeks,futures,physical,remain,continue,level,exhibiting,28,gold,prices	"Gold prices are set to drop next week with several analysts expecting the precious metal to continue exhibiting weakness after two weeks of muted values.

As many as 12 of 22 analysts polled in a Kitco Gold Survey said they expected gold prices to drop next week, while six predicted that prices would rise and four forecast prices to remain unchanged.

Lower prices could now boost physical demand.

Phillip Streible, senior market strategist at RJO Futures, said: "Gold futures should remain under pressure as long as the issues with Russia and the Ukraine fade and investors remain focused on the thoughts of tapering (stimulus) and rising interest rates,".

Kevin Grady of Phoenix Gold Futures and Options, said: "I still believe that the physical market is directing our underlying price.... In the gold forward rates we noticed that the physical tightness dropped off as we approached the $1,400 level. This situation put the shorts in control.

"We have noted that the rates have gotten tighter as we broke the $1,300 level. It appears that the price-sensitive buyers are back. We need to hold our major support level of $1,270 for gold to rebound."

Commerzbank Corporates & Markets said in a 28 March note to clients: "Gold not only dipped under the $1,300 per troy ounce mark [on 27 March] but also fell below the technically important 200-day moving average.

"Although the price closed beneath the 200-day moving average, there has been no technical follow-up selling so far. Gold ETFs recorded slight inflows again [on 27 March], holdings having been reduced in the two previous days.

"In other words, speculative financial investors are likely to have been mainly to blame for the price slide."

Gold Ends Lower

US Gold Futures for delivery in June finished 50 cents lower at $1,294.30 an ounce on 28 March.

Prices lost 3.1% for the week as a whole.

Earlier, spot gold inched up 0.2% to $1,293 an ounce.

Gold prices are down $100 from their price peak two weeks ago. Prices ended near six-week lows on 28 March, logging a second consecutive weekly loss.

Improving US economic outlook has supported the US dollar and has boosted the global appetite for risk, denting gold's safe-haven investment status."																					1	0	1
68192	Gold futures weekly recap, March 24 – March 28	http://www.binarytribune.com/2014/03/29/gold-futures-weekly-recap-march-24-march-28/	Binary Tribune	b	d_gVpCAKL5OJx5MwfYTkwNfgtpTYM	www.binarytribune.com	2014-03-31 03:54:25	1		en	spending,rose,data,economy,week,futures,showed,recap,ounce,24,weekly,months,gold,analysts	"Gold futures fell to the weakest level in six weeks on Friday, capping a second weekly loss, as further signs of recovery in the US backed the case for the Federal Reserve to keep cutting stimulus. Meanwhile, assets in the SPDR Gold Trust, the biggest bullion-backed ETF, remained unchanged on Friday.

On the Comex division of the New York Mercantile Exchange, gold futures for settlement in April rose 0.07% on Friday to settle the week at $1 295.70 an ounce. Prices shifted in a daily range between $1 299.40 an ounce and $1 286.40 an ounce, the weakest since February 13. Gold slid 3 percent this week, the second straight decline.

Bullion has retreated 7.1% since reaching a six-month high of $1 392.60 an ounce on March 17 as the US economy expanded at a faster-than-expected pace and Federal Reserve Chair Janet Yellen said the central bank’s bond-buying program may be brought to an end this fall, with borrowing costs starting to rise by mid-2015.

“Prices come under pressure when there’s a lack of concern about economic risks,” said Kevin Caron, a Florham Park, New Jersey-based market strategist at Stifel Nicolaus & Co., which manages about $160 billion, cited by Bloomberg. “There’s probably more weakness ahead.”

However, the precious metal rose 7.7 percent this quarter as global growth faltered and as turmoil over Ukraine left Russia and the West involved in their worst conflict since the end of the Cold War.

Fed stimulus outlook

Gold prices were pressured after data showed consumer spending in the US rose in February by the most in three months as incomes increased, adding to evidence the economy is gaining momentum after the unusually harsh winter.

Consumer spending, which accounts for almost 70% of the American economy, rose 0.3% last month, in line with analysts’ estimates and after a 0.2% increase in the previous month that was smaller than previously reported. Incomes also advanced 0.3% in February, in line with analysts’ expectations and matching January’s gain, data by the US Commerce Department showed today.

The US citizens were trying to shrug off the effects of the inclement weather as they rushed out to shop, supported by a labor market that was also gaining traction.

“Looking past some of the noise in the data, the trend is for modestly stronger personal income and spending, which should accelerate throughout the year as the economy builds momentum,” Michelle Meyer, a senior U.S. economist at Bank of America Merrill Lynch in New York, said before the report, cited by Bloomberg.

Friday’s data also revealed that core price, excluding the volatile food and fuel items, inched up 0.1% last month and were up 1.1% from the previous year, the same as in January and in line with analysts’ estimates.

Also fanning negative sentiment, the US economy expanded more rapidly in the final three months of 2013 than previously estimated as consumer spending jumped by the most in three years, while initial jobless claims unexpectedly declined last week, curbing demand for the precious metal as a store of value.

The US economy expanded at a 2.6% annualized rate in the final three months of 2013, slightly below analysts’ expectations of a 2.7% gain, but up from a preliminary estimate of 2.4%, a report by the the Bureau of Economic Analysis showed yesterday. The US gross domestic product grew 4.1% in the third quarter.

Assets in the SPDR Gold Trust, the biggest bullion-backed ETP, were unchanged at 816.97 tons yesterday. Holdings in the fund are up 1% this year after it lost 41% of its assets in 2013 that wiped almost $42 billion in value. A total of 553 tons has been withdrawn last year."																					1	0	1
68194	Gold Weekly Fundamental Analysis March 31 – April 4, 2014 Forecast	http://www.fxempire.com/fundamental/fundamental-analysis-reports/gold-weekly-fundamental-analysis-march-31-april-4-2014-forecast/	FX Empire	b	d_gVpCAKL5OJx5MwfYTkwNfgtpTYM	www.fxempire.com	2014-03-31 03:54:26	1		en	price,likely,analysis,selloff,steep,usdjpy,yields,treasury,risk,action,fundamental,toread,technical	"Based on Monday’s price action and the early action on Tuesday, it looks as if USD/JPY investors have absorbed the plunge in U.S. Treasury yields. It further indicates the next major move in the Forex pair will likely be determined by appetite for risk. Another steep sell-off is likely to

Read More"																					1	0	1
68197	Gold concludes week in loss	http://www.globaltimes.cn/content/851502.shtml	Global Times	b	d_gVpCAKL5OJx5MwfYTkwNfgtpTYM	www.globaltimes.cn	2014-03-31 03:54:27	1			data,rose,week,dollars,concludes,loss,economic,close,level,growth,delivery,gold	"Gold concludes week in loss

Gold futures on the COMEX division of the New York Mercantile Exchange closed lower Friday as US economy keeps recovering.



The most active gold contract for June delivery dropped 0.5 dollars, or 0.04 percent, to settle at 1,294.3 dollars per ounce.



Gold ended the week with a loss of 3.1 percent but concluded the first quarter of this year with a gain of 7.7 percent.



With eased tension in Ukraine, economic data again took hold of gold market. US Commerce Department reported Friday that US consumer spending rose 0.3 percent in February on a seasonally adjusted basis, the fastest growth since November. The upbeat economic data, together with a 2.6-percent US economic growth in the fourth quarter of last year and initial jobless claims touching the lowest level in four months, drew investors to equities from gold.



Even a report from the University of Michigan and Thomson Reuters putting the consumer sentiment gauge at a final March reading of 80, the lowest level since November, failed to prop up gold market.



The 1,300-dollar level is a psychological support for gold. Now thanks in part to strong economic data, this level has been broken. Market analysts believe that under the expectation for a rising U. S. dollar, the growth of gold will be limited this year.



Investors are also paying close attention to the US Federal Reserve's plan to scale back its bond purchases and eventually return to normal monetary policy.



Silver for May delivery rose 8.2 cents, or 0.42 percent, to close at 19.79 dollars per ounce. Platinum for July delivery climbed 8.8 dollars, or 0.63 percent, to close at 1,407.2 dollars per ounce.

"																					1	0	1
68203	Back to the Futures: Market stops yelling for gold, more beans	http://thegazette.com/2014/03/28/back-to-the-futures-market-stops-yelling-for-gold-more-beans/	The Gazette\: Eastern Iowa Breaking News and Headlines	b	d_gVpCAKL5OJx5MwfYTkwNfgtpTYM	thegazette.com	2014-03-31 03:54:28	1			market,farmers,rates,million,soybeans,prices,futures,acres,beans,stops,watching,corn,gold,yelling	"[Editor's note: Every Friday visit the Business 380 for "Back to the Futures," a quick discussion of the week's grain, livestock, gasoline prices and other topics.]

Market stops yellin for gold

Janet Yellen, in her first meeting as Chairwoman of the Federal Reserve last week, indicated that the Fed would continue to reduce stimulus and could be on track to start raising interest rates in the near future. In response, gold prices have collapsed, losing over $100 per ounce.

The Federal Reserve, through a series of programs, have lowered short-term interest rates to near zero and have pulled down long term rates as well, making it less expensive to borrow money. While these measures made mortgages and other loans cheaper, it also sparked fears that inflation could accelerate, which helped push gold over $1900 per ounce in 2011.

Yellens most recent announcement was taken as negative for gold, which hammered the metal down to $1286 on Friday, a six-week low.

Despite the potential bearish influences from the Fed, other gold investors are closely watching the situation in Ukraine. With as many as 50,000 Russian troops poised on the Ukrainian border, some market watchers believe that war could be brewing, which could cause global investors to flock towards the perceived safety of gold.

More beans please, hold the corn

On Monday, the US Department of Agriculture is going to release its annual Prospective Plantings report, which will outline expectations for this years crop acreage.

During the winter, farmers have been watching grain prices along with fuel, seed, and fertilizer costs so they can determine which crops theyll plant this year. Throughout much of the Midwest, many farmers simply split their acreage between corn and soybeans, but they can adjust acreage to capture greater profits, planting more of the high-margin crop.

Lackluster corn prices and strong demand for soybeans have encouraged some farmers to add as many as 5 million acres of soybeans, while dropping corn planting by nearly 3 million acres from last year. If these intentions hold true, US farmers are going to plant a record-breaking 81 million acres of beans this spring.

On Friday, as the markets were waiting for the USDAs figures, the new crop December corn was worth $4.88 per bushel, while November beans traded for $11.90."																					1	0	1
69701	Talking Dead Viewer Recreates Love Actually Scene for Andrew Lincoln	http://jezebel.com/caller-talking-dead-makes-awesome-love-actually-joke-1555045653	Jezebel	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	jezebel.com	2014-03-31 05:59:06	1		en	dead,talking,watch,dedicated,courtesy,viewer,fans,love,scene,good,walking,deads,andrew,actually,lincoln,recreates	"Love Actually fans got a huge surprise after tonight's Walking Dead finale in the form of a fan's adorable joke

People who watch The Walking Dead's after show call-in party, Talking Dead got a good laugh courtesy of a dedicated viewer named Heather Seebach, who runs a site called Viewer Discretion Advised. You'll recall the classic card-flipping Andrew Lincoln (aka The Walking Dead's Rick Grimes) played out for Keira Knightley in Love Actually. This time, the card flipping comes courtesy of one dedicated fan, who asks "which do you think is more challenging for Rick—being a good father or being a good leader?"

I'll let you watch the clip for the real "Awwwww" moment."																					1	0	1
69726	THE WALKING DEAD Season 4 Finale Poll & Discussion	http://www.comicbookmovie.com/fansites/movienewsandreviews/news/\?a=97145	Comic Book Movie	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.comicbookmovie.com	2014-03-31 05:59:12	1		en	series,poll,finale,season,kirkman,riggs,sonequa,yeun,steven,scott,walking,robert,discussion,dead	""The Walking Dead, the most watched drama in basic cable history, will return for a sixteen episode fourth season on October 13, 2013. Based on the comic book series written by Robert Kirkman and Charlie Adlard and published by Image Comics, The Walking Dead stars Andrew Lincoln, Steven Yeun, Norman Reedus, Chandler Riggs, Lauren Cohan, Scott Wilson, Melissa McBride, David Morrissey, Chad Coleman, Sonequa Martin-Green and Danai Gurira . The series is executive produced by Kirkman, Scott M. Gimple, Greg Nicotero, and Gale Anne Hurd."

Running Time:

Release Date:

TV Rating:

Starring:

David Morrissey

Creators:

Written by:

Rick (Andrew Lincoln) returned to being a stone-cold bad ass! The true nature of Terminus is revealed. But what about the fate of a couple of other survivors not shown in this episode. Did they survive? And how will Rick and co. get themselves out of their current pridicament. It's one thing to give bad ass statements to rally the troops and quie another to get yourself out of a box car and away from a compound full of cannibals. It's going to be a long wait till next October!60 minutes (45 min actual air time)October 2013 (Season 4-premiere)TV-MA for sex & nudity, violence & gore, profanity, alchohol/drugs/smoking and frightening/intense scenesAndrew Lincoln,,Chad Coleman, Sonequa Martin-Green, Steven Yeun, Chandler Riggs, Emily Kinney, Norman ReedusFrank Darabont (show) Robert Kirkman (comic)Frank Darabont, Charles H. Eglee, Jack LoGiudice, Robert Kirkman, Glen Mazzara, Adam Fierro, Charlie Adlard, Tony Moore, Evan T. Reilly"																					1	0	1
69727	'Talking Dead' finale: Andrew Lincoln says Rick Grimes is a 'changed man'	http://cartermatt.com/115392/talking-dead-finale-andrew-lincoln-says-rick-grimes-changed-man/	CarterMatt.com	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	cartermatt.com	2014-03-31 05:59:12	1		en	dead,chicken,need,talking,finale,man,grimes,rick,right,scene,changed,cartermatt,andrew,kept,lincoln	"







For the first time since the series first came on the air after new episodes of “The Walking Dead,” Andrew Lincoln actually showed up on “Talking Dead” Sunday night in order to do his best to explain what transpired … and also what is coming up for Rick Grimes.

The biggest thing we found out through all of this? That Lincoln is so committed to his craft that he is willing to stick raw chicken in his mouth for that biting scene with Joe. Here’s what he said to Chris Hardwick about it:

“Greg Nicotero kept sidling up to be in the week preceding this scene, and he kept saying ‘we need to talk about the [bite gag]. And he said, ‘chicken or beef?'”

Lincoln said that this scene was the real moment on the show where the Rick Grimes that we knew earlier on this season (which was the inspiration for the flashbacks) ended, and shows the contrast between where we were, and where we are now. Rick is a “changed man,” and that is good news for the rest of the survivors who are in desperate need of a hero. Right now, these people are in a pretty darn horrendous situation. They aren’t in a position to do anything other than trying to survive, and he can inspire them to fight back and take these people down. We just don’t think that it is going to happen for him right away. This plan, like many others, will likely take time.

What did you want to see from Rick Grimes next? As always, we want to hear your thoughts below! You can also visit the link if you want to get a few more news about what comes next, and here if you want to sign up for our CarterMatt Newsletter to get news on all things we cover.

Photo: AMC

Love TV? Be sure to like CarterMatt on Facebook for more updates!







"																					1	0	1
69729	All The GIFs From 'The Walking Dead' Season 4 Finale	http://www.uproxx.com/up/2014/03/gifs-walking-dead-season-4-finale/	Uproxx	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.uproxx.com	2014-03-31 05:59:12	1			thats,train,finale,hey,watch,gifs,season,turns,thoughts,twitter,walking,end,dead	"And here we are, the season finale of The Walking Dead. Let’s see what happens.

So it turns out that Daryl’s gang catches up with the Grimes.

It does not end well for the Claimers.

RELATED: 15 Twitter Responses To THAT Bad-Ass Kill In The Season Finale

So it’s on to Terminus.

It starts off OK, but hey, how’d that one guy get Hershel’s watch? Not cool.

Of course the resistance is futile.

And hey, look who they end up in train jail with. Aaaaand that’s your set up for next season.

Yup. Feel free to let loose with your immediate thoughts as Dustin will be here later to recap it all fully."																					1	0	1
69731	'Walking Dead' ends season 4 with a cliffhanger and fans react on Twitter	http://www.cleveland.com/tv/index.ssf/2014/03/walking_dead_ends_season_4_wit.html	The Plain Dealer	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.cleveland.com	2014-03-31 05:59:13	1		en	returns,finale,ohio,happen,group,season,react,rick,fans,rest,twitter,walking,ends,cliffhanger,dead	"WALKING_DEAD_RICK.JPG

What's going to happen with Rick and the rest of his group when "The Walking Dead" returns in October?

(Gene Page, AMC via Associated Press)

CLEVELAND, Ohio — After a season that some fans believed dragged, "The Walking Dead" ended its fourth season with an intense finale that finds Rick Grimes and the rest of his group in a tough situation.

We'll leave out the details for people who might not have seen Sunday night's finale. (Go here to see recap from Northeast Ohio Media Group's Troy L. Smith.) However, it brought a swift reaction on Twitter — and the "reviews" were all over the place.

See below for a sample of reactions from Twitter moments after the finale ended. Also, comment below on what you thought of the season and what you would like see happen when the show returns in October."																					1	0	1
69732	Create a custom date range	http://www.orlandosentinel.com/entertainment/blogs/tv-guy/os-walking-dead-bleak-final-stop-20140330,0,553897.post	Orlando Sentinel \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.orlandosentinel.com	2014-03-31 05:59:13	1			range,readers,website,provide,unavailable,region,currently,unfortunately,options,support,solutions,technical	Unfortunately, our website is currently unavailable in most European countries. We are engaged on the issue and committed to looking at options that support our full range of digital offerings to the EU market. We continue to identify technical compliance solutions that will provide all readers with our award-winning journalism.																					1	0	1
69735	15 Perfect Twitter Responses To THAT Bad-Ass Kill In The Season Finale Of  ...	http://www.uproxx.com/tv/2014/03/15-perfect-twitter-responses-bad-ass-kill-weeks-walking-dead/	Uproxx	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.uproxx.com	2014-03-31 05:59:14	1			used,thats,finale,badass,perfect,kill,thing,season,weapon,teeth,responses,twitter,walking,15,kills,dead	"RELATED: All The GIFs From ‘The Walking Dead’ Season 4 Finale

If you were on Twitter around 22 minutes into the fourth season finale of The Walking Dead, then you likely saw it explode after one of the most bad-ass kills in The Walking Dead’s run. It was one of those kills that make you pump your fist, and that make you see a character in a completely different light. Twitter was impressed, that’s for damn sure.

SPOILERS BELOW

At 9:22 EST, in order to save himself, Carl, Michonne, and Daryl from the marauders, Rick — without a weapon — used the only thing he had at his disposal: His teeth. He f**king ripped out Joe’s neck jugular WITH HIS MOUTH. And it was insane.

Here’s how Twitter responded."																					1	0	1
69745	Discuss Tonight's Walking Dead Season Finale!	http://io9.com/discuss-tonights-walking-dead-season-finale-1554961701	io9	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	io9.com	2014-03-31 05:59:16	1		en	warned,finale,tonights,season,thoughts,weve,tomorrow,terminusbut,screams,walking,discuss,spoilers,dead,comments	"The Walking Dead has arrived in Terminus—but that doesn't mean we've found sanctuary. And you can chat about tonight's episode right here.

We'll have our recap up tomorrow morning, but in the meantime, post your thoughts and screams of anguish in the comments. And be warned: you should expect spoilers in the comments."																					1	0	1
69746	The Walking Dead: Season 4 Finale is Here - So Who's Dying?	http://www.ign.com/articles/2014/03/30/the-walking-dead-season-4-finale-is-here-so-whos-dying	IGN	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.ign.com	2014-03-31 05:59:16	1		en	tragedy,finale,glenn,shows,season,reunion,getting,tonight,theyre,right,walking,happy,dead	"Share. Come on, they're not all just getting a happy reunion, right? Come on, they're not all just getting a happy reunion, right?

The Walking Dead: Season 4 finale is airing tonight on AMC and if this show's history is any indication, at least one character won't be making it out alive. As all our characters are finally coming back together, tragedy just has to be around the corner again, right? So who's it going to be? One of the more recent introductions, like Abraham, Rosita or Eugene? A mainstay from the show's earliest days like Glenn or Carol? Did Glenn and Maggie's happy reunion instantly mean tragedy is around the corner for one of them? Perhaps the show might really go for the jugular and kill Rick or Carl or, gasp, Daryl. Or will our heroes get through this one relatively unscathed and Joe and his gang will meet their likely inevitable end?

Let us know and look for our review of the finale later tonight, after we've seen the west coast airing of the show."																					1	0	1
69748	The Walking Dead: Five Questions The Finale Must Answer	http://comicbook.com/blog/2014/03/30/the-walking-dead-five-questions-the-finale-must-answer/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:17	1		en	answer,finale,things,kirkman,pretty,rick,beth,questions,place,walking,trap,judith,terminus,dead,hunters	"With less than an hour left to go before the season finale airs on the East Coast of the United States and spoilers start to flood social media, there are some things that pretty much every fan wants to see, or have answered, in tonight's episode, which is intriguingly titled "A."

What are the "If you _________, we will riot!" story beats for tonight? Read on...

Will Rick and Judith be reunited? Ever since the fall of the prison, Rick and Carl Grimes have believed that Judith -- Rick's one-year-old daughter and Carl's baby sister -- died in the siege on their former home.

Unbeknownst to them, the baby was saved by Tyreese, who What happened to Beth?

Shortly before Daryl joined up with Joe and the other members of his gang, he and Beth were traveling together when they wandered into a house that, in hindsight, seems like a pretty obvious trap. A well-stocked building with supplies and a booby-trapped field not far away was an enticing place to hole up for a day or more...until a stream of walkers found their way directly in the door and the pair became separated. The last Daryl (or any of the viewers) saw of Beth, she had apparently been taken away in a mysterious car. Since then, we've had no inkling who might have been driving the car or what business they have with Beth. One of the early popular theories was that it was The Hunters, but it seems that now most fans think The Hunters will be the people living in Terminus, and Beth's captor will likely be someone else entirely. Could it turn out to be someone...not so bad?! Yeah, we doubt it, too.

What is Terminus? This one is bound to be answered, probably fairly quickly. Most fans assume that Terminus is pretty terrible, in no small part because that's what creator Robert Kirkman said he would put his money on if he were a betting man. Of course, just about every new development in The Walking Dead is a big, glowing sign that says "things are gonna get worse," so even if Kirkman hadn't said that, it wouldn't be much of a stretch to expect that the place where "those who arrive, survive" is a giant trap."																					1	0	1
69750	The Walking Dead Finale Spoiler: Dead Character Returns	http://comicbook.com/blog/2014/03/30/the-walking-dead-finale-spoiler-dead-character-returns/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:17	1		en	returns,character,finale,workswalking,tv,interesting,kirkman,opening,tonight,spoiler,walking,heres,twitter,dead	"Here’s an interesting tidbit of information dropped during a pre-finale official Walking Dead Twitter Q&A. A fan asked, “Is there a Hershel flashback in the works?”

Walking Dead creator Robert Kirkman responded, “RT MAYBE TONIGHT!” While Kirkman could have been teasing, it’s interesting because there has been an opening spoiler floating around, which came from an Australian TV newspaper called Border Mail. Here’s the opening description."																					1	0	1
69751	Talking Dead Episode 16 Season 4: Andrew Lincoln, Scott Gimple, and Mystery  ...	http://www.theepochtimes.com/n3/591919-talking-dead-episode-16-season-4-andrew-lincoln-scott-gimple-and-mystery-guest-number/	The Epoch Times	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.theepochtimes.com	2014-03-31 05:59:17	1		en	dead,talking,gimple,number,cohan,grimes,season,episode,scott,twitter,guest,mystery,lincoln	"Talking Dead Episode 16 Season 4: Andrew Lincoln, Scott Gimple, and Mystery Guest (+Number)

Andrew Lincoln (Rick Grimes) and executive producer Scott Gimple will be guests on Talking Dead after The Walking Dead season 4 episode 16 on Sunday night. There will be a third mystery guest.

The mystery guest could be Lauren Cohan (Maggie), who was spotted at Los Angeles International Airport with Lincoln on Sunday.

On the other hand, James Vanderbeek was also in the video from the airport, and he likely won’t be a guest, so it could have just been a coincidence or something else. Lincoln and Cohan could have been returning from some sort of event together.

Still, Cohan could be on–and that could mean that something happens to her character in the finale.

The guest will not be Chandler Riggs (Carl Grimes), who took to Twitter to lament that AMC told him he wouldn’t be a guest.

Submit questions online by calling 1-855-332-2548, or visit the Talking Dead website, Facebook, or twitter page."																					1	0	1
69753	The Walking Dead: Five Threats We Might See In the Finale	http://comicbook.com/blog/2014/03/30/the-walking-dead-five-threats-we-might-see-in-the-finale/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:18	1		en	governor,finale,characters,group,threats,invaders,family,rise,walking,terminus,dead,hunters	"First of all, while we all turned out to be wrong at the time, comic book readers were pretty sure we had an inkling how the battle at the prison was going to go down, since there was a comic book corollary that followed very much the same basic arc that the second half of last year had done. There's no such parallel for Terminus, for Gareth (whoever he is) or for Joe and his merry band of Claimers.

Basically, the biggest question marks of the night -- we won't even say threats, since one or more of those may not turn out to be objectively bad -- are very up in the air this season.

Cannibals There are two distinct groups of cannibals in current The Walking Dead lore. We're expecting to see one, the other or maybe a merging of the two.

Around this time in the comics, the characters were heading into the “Fear the Hunters” storyline, in which a cunning group of cannibals secretly tracked and stalked a number of the characters. They attacked Glenn and ultimately managed to kidnap and partially eat Dale (he lasted longer in the comics, for you TV viewers). The Hunters (more on them here) were the first major enemies to come after The Governor, and their appearance tied together a lot of things that were going on at the time; a vicious turn Rick took when a group of highway bandits tried to assault Carl (more on that below, or here) tied together with the merciless way the survivors dispatched The Hunters to show a more proactive and violent side to our heroes…something that was playing off of the then-fresh death of Lori and Judith Grimes (among others) during The Governor’s siege on the prison.

The other possible group is a family of cannibals operating out of the St. John Dairy Farm. It's been noted that Mary from Terminus looks a bit like the family's matriarch, Brenda. The St. John cannibal family are characters original to the video games, who appeared in Telltale Games’ The Walking Dead: Season One episode "Starved For Help,” and seem much likelier candidates to be the denizens of Terminus than do The Hunters in that they make a facade of friendliness and pick off survivors quietly by pretending to be giving them medical help and other benign or even kind acts to peel them away from the group. The Home Invaders

In the novels based on the rise and fall of The Governor, there was a group referred to only as the "Home Invaders." Tommy is the leader of a group of home invaders who attempted to take the Peach Orchard house away from the Blake (The Governor) family and Nick Parsons in The Walking Dead: Rise of the Governor. It's virtually impossible that these characters will be used or important, but they're mentioned for two reasons: first, Robert Kirkman referred to Joe's group as "home invaders" after their first appearance in the episode titled "Claimed" and second, elements of Rise of The Governor and its follow-up novels, particularly The Governor's adoption of a false name and an emphasis on more of his family backstory, have been incorporated into this season of The Walking Dead."																					1	0	1
69762	'Walking Dead' or 'Walking Dread'?	http://www.newsforshoppers.com/walking-dead-or-walking-dread/36719286/	News For Shoppers	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.newsforshoppers.com	2014-03-31 05:59:20	1		en	dread,characters,little,season,episodes,zombie,thoughts,lull,really,writers,walking,dead,think	"If you are a fan of the series “The Walking Dead” you are probably feeling a little like the characters in the show: lost.

Yes, the show has started off the second half of the 4th season a little slow. The separation of the group has many viewers craving more and ultimately wanting the prison back.

But are these episodes really just the writers’ idea of a cruel joke or are they necessary to propel the show to new levels?

Every show goes through a lull period. Sometimes it is due to lack of ratings but sometimes, which is possible in the case of the zombie-laced show, the lull is really just a step into cementing the show into television history.

If you think about it, a lot has happened in the first four seasons.

Nearly a dozen main characters have been murdered (not to mention beheaded), a farm and a town have both burnt down, and the Governor has gone from crazy, to sane back to crazy, and finally dead.

The writers’ might think that the characters deserve a little downtime to gather their thoughts and get to know their inner zombie (because as we know…SPOILER ALERT…. everyone has the zombie gene inside them). Perhaps a little relaxation could be just what these characters need to get the energy and the action back.

In the last two episodes, they have really stepped it up.

They even had a preteen psycho kill her kid sister and then innocently proclaim, while holding a blood-soaked knife, that she was saving her.

Last weeks episode finally has part of the group finding their safe-haven. These two episodes may be a hint that the season finale is going to blow our minds.

Guess we will just have to wait and see.

What are your thoughts on tonight’s season finale?"																					1	0	1
69764	Most gripping moment on 'Walking Dead' in 2014? Take our poll before tonight's  ...	http://www.al.com/entertainment/index.ssf/2014/03/most_gripping_moment_on_walkin.html	al.com	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.al.com	2014-03-31 05:59:21	1		en	lizzie,poll,views,finale,recent,tonights,second,season,moment,peletier,weve,episode,gripping,walking,samuels,viewers,dead	"Bored with the slower pace? Or engrossed in character development?

Fans of

have found the second half of Season Four to be a polarizing experience. After the

on Dec. 1, the last seven episodes have struck some viewers as, well, rather tame.

Yes, we've seen gruesome zombie attacks. Plenty of blood has been splattered across the screen. But the

has altered its focus somewhat, splitting up the key group of survivors and giving viewers a closer look at the characters and their backstories.

On an episode titled "The Grove," characters on "The Walking Dead" were enmeshed in a psychological crisis. Carol Peletier (Melissa McBride, top) and Lizzie Samuels (Brighton Sharbino, bottom center) grappled to reconcile different views of the Walkers. Are the zombies horrible monsters or misunderstood friends? Lizzie opted for the latter. (AMC photos)

Tonight's season finale, "A," promises to bring naysayers back into the fold.

, creator of

and TV show, pegged the episode as "brutal" during a recent "

Series star Andrew Lincoln, who plays

, agreed with Kirkman during a

.

“I will say that something happens in the finale that when I read it, I called Scott Gimple, the showrunner, because we’ve always been incredibly responsible with the violence in this show," Lincoln said. "And I just wanted to ask, ‘Is this a step too far?’”

Of course, it hasn't been all sunshine and bonbons in recent weeks, especially during an episode called "The Grove." Two young sisters, Lizzie and Mika Samuels, found a temporary respite in a farmhouse with their adult protectors, Carol Peletier and Tyreese. Then everything went bonkers.

As tonight's 8 p.m. program approaches, let's take a look at some of the more gripping moments of Episodes 409-415. Which one made you gasp? Share your views in the poll below. If we've missed your favorite shocker in the second half of Season Four, tell us about it in the comments section.

awaits!"																					1	0	1
69766	The Walking Dead: Who Is Gareth?	http://comicbook.com/blog/2014/03/30/the-walking-dead-who-is-gareth/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:21	1		en	st,tv,dont,farm,dairy,version,gareth,fans,walking,john,terminus,dead,hunters	"Warning: What comes next is a mix of speculation and actual spoilers. If you don't want to be spoiled, don't continue down the page.

Because of the "major player" thing combined with the "nobody has seen him yet" element, most fans have figured that he will be a fairly major figure at Terminus, where we've been headed for the entire second half of the season.

It appears they're right, as an overseas TV spot for the episode features Gareth greeting Rick, Carl and Michonne at Terminus -- although not everything goes well (shocking, of course). We don't know a whole lot about his character, but we'll go on what we do know here, and try to make some educated guesses.

A TV version of Chris (leader of the Hunters) There is at least one armed gunman atop a building in Terminus, who fires down at Rick, Carl and Michonne when Gareth drops his hand (from the wave/salute shown above). This not only suggests generally that he's set a trap, but more specifically some fans have suggested it's reminiscent of something that Chris, the leader of The Hunters, did in the comics.

The group, a roving band of cannibals, were headquartered out of an isolated, rural house in the comics. They would stalk, trap and kill other survivors for their meat, eating them slowly and putting tourniquets on their wounds so that their victims would last longer in a world without refrigeration. Keeping their victims alive as long as possible also had the added benefit of preventing them from reanimating before the meat was off the bone. The Hunters first appeared in the comics at around the same time that Billy and Ben died (characters who have TV counterparts in Lizzie and Mika, who were killed in "The Grove" two weeks ago). As such, each new group to pop up has been greeted with "will they be The Hunters?" questions from fans...but in fact it seems likely that The Hunters will be merged with the St. John Dairy Farm cannibals from the Telltale Games series and allow the TV series to have a version of the story all their own that can incorporate the best elements from each of the two previous "cannibal" storylines.

Andrew or Danny St. John Of course, that being said, he could just as easily be a take on one of the St. John boys (cannibals from the St. John Dairy Farm and sons to Brenda, who many fans think could be the physical inspiration for Mary's character design), or the TV version thereof. Like Terminus, the St. John Dairy Farm has more creature comforts than most locales in The Walking Dead, including a generator to give some electricity. The brothers are essentially farmhands, helping their mother since their father isn't around (probably dead) and, well, zombie apocalypse and all. Cuts down on career prospects."																					1	0	1
69767	The Walking Dead Season Finale Preview	http://earsucker.com/the-walking-dead-season-finale-preview-44257/	earsucker	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	earsucker.com	2014-03-31 05:59:22	1		en	preview,various,celebrities,finale,season,loves,sites,walking,reddawnstatejed,writing,dead	"reddawnstate

Jed loves writing about celebrities and has been writing for various sites for over 10 years."																					1	0	1
69774	'The Walking Dead' season 4 finale spoilers: Andrew Lincoln, Chandler Riggs in  ...	http://cartermatt.com/115316/walking-dead-season-4-finale-spoilers-andrew-lincoln-chandler-riggs-photos/	CarterMatt.com	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	cartermatt.com	2014-03-31 05:59:23	1		en	finale,tv,photos,chandler,terminus,bit,updates,season,riggs,unfold,lincoln,sure,spoilers,dead,going,share,stuff,walking,andrew	"







On AMC Sunday night, you better get ready to see some truly crazy stuff unfold courtesy of “The Walking Dead’s” season 4 finale. Let’s just say that the story is for sure going to be a heck of a lot more exciting than the episode’s incredibly-boring name of “A.”

The network is as always being extremely careful on what they choose to share with the viewing public, and in this case, all they are handing down are some isolated photos of Rick (Andrew Lincoln) and Carl (Chandler Riggs). Clearly, these two plus Michonne (Danai Gurira) are going to have a very big role to play in the story. While the network has omitted certain stories in the past when it comes to their promotional material, they never necessarily mislead when it comes to who is going to be important. Given that these three characters have yet to make it to Terminus, and Rick doesn’t know that the Claimers are after him, all of this makes a great deal of sense.

As for some other important stuff that is going to be coming up, you will see a good bit more of life within Terminus for some of the people who are already there. This includes meeting some new faces, including some who are going to be around for quite a bit in the fifth season. We hope that the true motivations of this community are made a little bit clearer before the story winds down to the end, mostly because these people cannot be the masters of salvation that they have projected themselves to be in all their advertisements … right?

What do you think is going to unfold during this big episode? Share your thoughts below, and also be sure to click here in the event that you want to read some more news related to the huge episode. You can also sign up to grab some more TV updates from our CarterMatt Newsletter that are worth a celebration or two (or three).

Photo: AMC

Love TV? Be sure to like CarterMatt on Facebook for more updates!







"																					1	0	1
69775	The Walking Dead: Who are the Cannibals?	http://comicbook.com/blog/2014/03/30/the-walking-dead-who-are-the-cannibals/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:23	1		en	st,lot,cannibals,group,survivors,dairy,walking,john,terminus,games,dead,hunters	"It kind of makes sense; around this time in the comics, Rick Grimes and his merry band of survivors were heading into the "Beware the Hunters" storyline, in which a cunning group of cannibals secretly tracked and stalked a number of our characters. They attacked Glenn and ultimately managed to kidnap and partially eat Dale (he lasted longer in the comics, for you TV viewers).

The Hunters were the first major enemies to come after The Governor, and their appearance tied together a lot of things that were going on at the time; a vicious turn Rick took when a group of highway bandits tried to assault Carl tied together with the merciless way the survivors dispatched The Hunters to show a more proactive and violent side to our heroes...something that was playing off of the then-fresh death of Lori and Judith Grimes (among others) during The Governor's siege on the prison.

After Rick's attack on the Marauders, the battle between the Survivors and the Hunters put nearly everyone on edge for a while, wondering whether their response was justified and whether they were any better than the walkers, or any of the other survivors they'd killed along the way. It was a question that would hang over the group for a while, and really only be (completely) resolved a few years later when Negan came around and was self-evidently worse than any of our characters could ever hope to be (although it's not like there was a lot of navel-gazing and debate about it that whole time). We've talked a lot about The Hunters all season long, anticipating their arrival and speculating as to whether each new group of seemingly-menacing survivors might turn out to be cannibals as a result.

Now, with the finale on the horizon, it's worth noting that last week's first glimpse of Terminus was actually less reminiscent of the Hunters from the comics and another group of cannibals from the Telltale Games series. A number of fans in our comment threads and on message boards around the Internet have noted that Mary from Terminus bears a passing resemblance to Brenda St. John, the matriarch of a family of cannibals operating out of the St. John Dairy Farm.

She and her family are characters original to the games, who appeared in Telltale Games' The Walking Dead: Season One episode "Starved For Help," and seem much likelier candidates to be the denizens of Terminus than do The Hunters. Aside from the fact that, like Mary, she's a slightly-older-than-middle-aged woman who's kind and welcoming to strangers, there's the fact that the St. John Dairy Farm cannibals operate out of (wait for it) the St. John's Dairy Farm. It's a single, central location for their operations and rather than hunting people and then taking victims back home as the Hunters did, they allow people to come to them. While Terminus is a destination, the St. John Dairy is a bit more centrally located on the road and can take advantage of injured travelers who, upon arrival, can be easily separated from their group under the guise of providing medical care. In the video game, that's Mark; in the TV series, the most likely candidate seems to be Tara if that particular plot beat were to be replicated."																					1	0	1
69777	The Walking Dead Finale Spoiler: Possible Talking Dead Mystery Guest Hints At  ...	http://comicbook.com/blog/2014/03/30/the-walking-dead-finale-spoiler-possible-talking-dead-mystery-guest-hints-at-surprise-death/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:24	1		en	andrew,talking,finale,told,lincoln,weeks,cohan,riggs,amc,surprise,guest,spoiler,walking,hints,possible,mystery,dead	"Spoiler Warning: While the information contained in this article is not a definitive spoiler for The Walking Dead Season 4 Finale, it does present some information, which might suggest a surprise death on the finale.

Last week, Chandler Riggs asked AMC to be a guest on this week’s episode of Talking Dead. Riggs was already scheduled to be in California for a convention, so AMC wouldn’t have even needed to fly him in for the show. Chris Hardwick told Riggs that he was welcome on the show any time, but AMC ultimately told Riggs that he couldn’t be on this week’s Talking Dead.

Why would AMC turn down Chandler Riggs? Andrew Lincoln and Scott Gimple are the only announced guests for this week’s Talking Dead, and the show often has three guests. While there has been much speculation over if AMC might have not wanted a child actor on the Talking Dead due to some controversial scenes in the Season 4 Finale, another logical explanation could be that there is already a third mystery guest booked to be on the Talking Dead. Yesterday, video surfaced online of Andrew Lincoln and Lauren Cohan arriving at LAX airport in Los Angeles, California. Of course, Andrew Lincoln is scheduled to be on the Talking Dead. Could Lauren Cohan be a mystery guest on the Talking Dead? Cohan does seem to be making more effort to avoid the photographers than Lincoln."																					1	0	1
69778	The Walking Dead Poll: Would you have gone to Terminus?	http://smallscreenscoop.com/the-walking-dead-terminus/339435/	Small Screen Scoop	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	smallscreenscoop.com	2014-03-31 05:59:24	1			poll,screen,picked,wouldnt,gone,place,small,walking,fun,terminus,wrongly,dead	"March 30, 2014 at 1:13 PM EDT

Before we find out what the deal with Terminus is, pick a side now.

The Walking Dead Poll

If you were one of our characters on The Walking Dead, what would you have done when you saw the signs for “Terminus” on the railroad?

If you go, it may end up being a haven. After all, “Those who arrive, survive.” In the previous episode, Terminus looked like a pretty great place to be. They even had a personal chef station. Carve me up some rabbit.

However. If the place ends up being a cult of cannibals, I wouldn’t be surprised. After all, it is The Walking Dead that we’re talking about.

Before we know how this will play out, place your bets.

(Poll below.)

subscribe now: small screen scoop

follow the tv blog on twitter: @ssscoop

facebook more your style? small screen scoop on FB

Thanks for answering the poll. Share it around and let’s see what everyone would have picked. Then we can make fun of anyone who picked wrongly. Fun times, my dudes."																					1	0	1
69779	Someone Will Die On Tonight's "The Walking Dead" Finale. Bets Are On	http://www.contactmusic.com/article/norman-reedus-walking-dead-finale_4131704	Contactmusic.com	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.contactmusic.com	2014-03-31 05:59:25	1		en	reedus,finale,writing,tonights,popular,big,favorite,zombie,twd,die,team,walking,terminus,bets,dead	"It’s time for the hotly anticipated Walking Dead season finale tonight – yes, time sure does fly, when you’re watching people fight off a global zombie plague. This one’s big, as we’ll finally see the band of survivors arrive at Terminus – the sanctuary we’ve been hearing about for months. The place is rumored to be a walker-free haven for anyone, who survives the perilous trip to its gates.



Even universal favorite Daryl might not be safe.

Of course, in TWD, as in life, everything comes at a price. The big questions now are: Is Terminus really what it promises to be? If so, how has it stayed that way? And most importantly: which members of the prison team will even make it there? It sounds almost too good to be true. Given the writing team’s tendency to go for surprise plot twists of the bloody variety, the team might be about to have the rug pulled out from under them. It has happened before *cough* Governor *cough*.

Ahead of the big episode, E! have released a special poster, featuring everyone’s favorite zombie killer, Daryl (Norman Reedus). It’s beyond us how he manages to look that cool during a zombie Apocalypse, but the bigger question right now is: what will he have to do to protect his new family?



Or it might be Carl. Please let it be Carl.

Executive producer Robert Kirkman said in a Reddit AMA last week, "In my opinion, I feel like characters ripen like fruit. So while I wouldn't say the more popular a character is the more likely they are to die, they do have to reach a certain level of popularity before they've ‘earned' the death. No character is too popular to die. (Suck it, Reedus!)" What do you think – is it just hype, or would the writers actually go through with it?



Note to writing team: needs more Michonne.

Read more: What's wrong with TWD these days?"																					1	0	1
69780	Talking Dead Live RECAP 3/30/14: With Andrew Lincoln and Scott Gimple	http://www.celebdirtylaundry.com/2014/talking-dead-live-recap-33014-with-andrew-lincoln-and-scott-gimple/	Celebrity Dirty Laundry	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.celebdirtylaundry.com	2014-03-31 05:59:25	1		en	dead,talking,live,gimple,33014,asks,season,recap,rick,mentions,episode,scott,chris,andrew,lincoln	"Talking Dead returns this evening on AMC at 10PM EST and this week’s guests include Andrew Lincoln and Scott Gimple. Did you watch the last episode of Talking Dead? The special guests were Steven Yeun and Josh McDermitt and we recapped it right here for you so if you missed it then check it out!

Talking Dead features host Chris Hardwick who also hosted Talking Bad. Chris will spend time with fans, actors, producers and tv enthusiasts, recapping tonight’s TheWalking Dead episode, and taking questions and comments from viewers. Fans may continue to engage with the after-show following the on-air conclusion, online, at AMC.com for more videos, weekly polls and photo galleries of the guests featured on the series.

Tonight’s episode will feature the special guests discussing the new episode, “A” in detail. Will all our favorites survive tonight’s finale. We’ll find out on tonight’s episode and then get to dish all of the inside details with Andrew Lincoln and Scott Gimple afterwards. Since Andrew plays Rick on The Walking Dead they should have a lot to say about the episode. Scott is a writer on NBC’s Life and Fox TV’s Drive, and ABC’s FlashForward.

The Talking Dead begins at 10PM EST and we’ll be recapping it for you right here. AMC asks viewers to submit questions in advance so what are you the most curious about this season? Hit up the comments and tell us!

While you wait for the recap of Talking Dead, Celeb Dirty Laundry offers a live recap of tonight’s The Walking Dead Season 4 Finale. [CLICK HERE]

RECAP: Chris welcomes Andrew Lincoln and Scott Gimple, Chris asks how Rick has changed Andrew. Andrew says he is a lot darker as a human being and that he has had his confidence immensely and it wearing a new set of cowboy boots; Scott says it’s been the same boots the whole series. Chris asks for them and Andrew tells him that he really doesn’t want them; Chris says that Rick is just changing the whole time. Andrew says it’s amazing to be a character for four years and that there is a bunch of turning points and loves playing a character that is transforming continuously; he believes this episode shows that Rick has become a brutal person to protect those he loves. Scott mentions how they saw them at the car covered in blood; Rick wasn’t regretting anything. He doesn’t let the violence get to him no longer and knows he has to do what he must; kind of like waking up and figuring out what he must do. Scott says Rick has gone through so much that he can now accept himself. Chris asks what they planned with this season; Scott mentions to give each character a story to find out more about each of them.

Chris asks what the symbol of the flash backs; Scott says it was to show his journey how he used to be less aggressive by Hershel’s teachings. Though that world is over and Rick is now in an entire scene; Andrew mentions that Scott Wilson who plays Hershel is a legend. Andrew says he loved seeing his pony tail and hobbling around; Scott mentions how he told Scott Wilson to never cut his hair or shave his beard after the show because he thought he may use him again. Scott mentions that he was happy he didn’t shave; it would have made things much harder.

Chris asks Scott what made him write the ambush scene; Scott says it was straight from the comics. They made it reimagined into their story, it is the moment of transformation for Rick; it makes him a warrior. Chris says he got so excited to see Rick bite the guys throat; Scott says that he wanted the audience to get super pumped up about the fight but weird at the throat bite. Andrew says that when he read the script and felt they may have been crossing the line of violence in the show with the bite. Andrew says that after he did the scene it made complete sense to him; Andrew chose chicken and actually went ahead and bit some raw chicken as the neck. Chris says it was so wonderful; the whole time you watch the show and made him realize how Rick basically took the walker approach with the bite.

Chris asks what is the significance to Rick calling Daryl his brother; Andrew believes that it’s the ultimate alpha male thing to say. Like it’s saying I love you and trust you completely; Chris feels like Daryl now has another older brother. Andrew mentions how the rag had no water on it; he was just rubbing it against his beard. Chris asks what is with Michonne talking to Carl about what she did in the past; Scott believes that it is to tell Carl to not think of his father as a monster. Andrew mentions that he feels that Carl may be afraid of his father; though at the first scene at Terminus and how Carl is getting to understand him more. A fan asks what’s Rick’s biggest regret in the apocalypse; Andrew says he doesn’t regret anything. He makes the choices to stay alive and that right now he is much stronger and lethal; having made peace with the brutality within him.

Chris says that next season they will have Chandle Riggs who plays Carl on the show next season, Chris gets a Skype question from a fan named David; he asks Andrew what celebrity he would love play themselves in The Walking Dead. Andrew says he would love to see William Shatner. A video message from Christian from Norway; he asks what was the biggest lost this season Hershel or the prison. Andrew says that it was obviously Hershel for everybody though the second part of the season they all have his memories to carry themselves to keep in living from his teachings. Another live caller called Jessica ask Andrew when he was running through Terminus and that it looked like it was non-stop; Andrew says at one moment Norman took his crossbow and threw it on the ground. Andrew mentions how he wanted to kill someone the whole time. A fan asks what advice Rick from the apocalypse would give Rick before it all; Andrew says he’d tell him to not wake up. Scott says that he would tell him about how bad things do get.

Chris asks Andrew if it was hard to nail the final word of the season; Andrew says that there was another word and that the comic readers would know about it. Andrew says it was spicy and it was an F-bomb; he wishes he could have used it. Scott says that for families and that people can change the words; Chris says that was the emotions from the word. Andrew says he was embarrassed shooting that scene; he was punching the ground to pump himself up to not mess it up. Scott says that every 8 episode reinvents itself and it’s exciting; though next season will feel like a whole new show. It’s going to be a nuclear weapon; Chris shows off a special hoodie everyone in the audience is getting.

A fan asks if Rick will have hope for a sanctuary and Andrew mentions that it drives him; the prison was close but the pesky governor ruined it all. Chris asks how as an actor what is Andrew taking into it; Andrew says he needs to grow his beard and that he is going to listen to a lot of ACDC and flip tables. Andrew can’t wait to go back to Atlanta and see his family as well; he honestly loves what he is doing. Chris asks Scott how he feels about the next season; he says that they are really happy about it and they feel like it’s going to incredible. Andrew says that their head of make up is not coming back season and thanks her for all her amazing hard work."																					1	0	1
69783	THE WALKING DEAD Season Four Finale Preview	http://www.welovesoaps.net/2014/03/the-walking-dead-season-four-finale.html	We Love Soaps	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.welovesoaps.net	2014-03-31 05:59:26	1		en	preview,1979,soap,st,finale,lights,today,soaps,season,history,love,opera,kristoff,walking,john,heart,dead	"Today in Soap Opera History (March 21) 1979: Guiding Light's Jackie wanted Alan to keep her secret. 1980: J.R. Ewing was shot on the third season finale of Dallas . 2005:...

Daytime Emmy Nominations: 'Days of our Lives' Leads Daytime Dramas, 'Giants' Tops Digital The National Academy of Television Arts & Sciences (NATAS) today announced the nominees for the 46th Annual Daytime Emmy® Awards. The c...

Today in Soap Opera History (March 22) 1962: Ann Flood debuted as Nancy on The Edge of Night . 1983: General Hospital's Jimmy Lee denied having Tolliver's papers. 199...

Today in Soap Opera History (March 20) 1953: Love of Life's Vanessa waited for news about Beanie. 1987: ATWT's John pulled Lucinda into a hot tub, then married her. ...

Kristoff St. John Cause of Death: Hypertrophic Heart Disease Kristoff St. John died from heart disease, and accidental alcohol overdose, according to a report from the L.A. coroner's office. The...

Today in Soap Opera History (March 19) 1979: Another World's Alice wasn't sure she should marry Dan. 1979: Guiding Light's newly arrived Ross rook Roger's cas..."																					1	0	1
69784	What a drag! 'Walking Dead' has been as sluggish as zombies	http://www.today.com/entertainment/what-drag-walking-dead-has-been-sluggish-zombies-2D79455428	Today.com	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.today.com	2014-03-31 05:59:26	1		en	need,drag,characters,daryl,zombies,season,episodes,rick,wouldve,carl,walking,sluggish,dead	"share tweet pin email

By all accounts, "The Walking Dead's" fourth-season finale is going to be epic. Words like "bloody," "deadly," "shocking" and "savage" have been thrown out by the executive producers.

Here's hoping it's a payoff worth all the hours viewers have invested in what has oftentimes been an almost insufferably slow and sluggish season.

Yeah, yeah, yeah. "The Walking Dead" is a character-driven drama, not a horror show with nonstop action and cheap thrills. Hey, we're huge fans too, but if we care more about the walkers than the humans to which entire episodes devote, then that's a a bit of a problem — and here are the issues that seemed to drag things down the most.

Today Who would've thought Rick Grimes would've ever sunk so low on "The Walking Dead"?

Man up, Rick. Seriously.

In the midseason premiere, "After," Rick had barely survived hand-to-hand combat with the Governor only to endure another power struggle — this time with his son. Barely able to walk, Rick trailed after Carl like a defeated parent at the grocery store with a whiny 4-year-old demanding sugary treats in every aisle.

His lowest point during the season was cowering under the bed while Joe's marauders fought over who had "claimed" the mattress. Rick was utterly defenseless, having given his only weapon to Carl, who was out foraging for food with Michonne. Brilliant — leave a recently comatose man alone without a gun while you two enjoy a ramble around the countryside and playing with Crazy Cheese! Sure, the former sheriff's deputy did manage to escape, but at what price? The psychopaths Daryl's palling around with are now hell-bent on killing him — or worse.

Alpha-male Warrior Rick is much more fun to watch than Farmer Rick (or even Bonkers Rick). Can this Humpty Dumpty of a man put his pieces back together again in time to save his gang from whatever awaits them at Terminus? Or will he just tend to the pretty flowers?

Puddn'head Grimes

If Joe's gang does square off against the Grimes group, let's hope the first thing they claim is Carl's dirty ol' Stetson. Honestly, if that kid were wearing a Braves cap, we'd dislike him 28 percent less. The boy's rite-of-passage episode, "After," was downright infuriating — like Carl's short supply of bullets, Chandler Riggs simply doesn't have the acting ammunition to pull off those weighty monologues. Michonne seems to like him, so he must have some redeeming qualities. In fact, if we need Carl to bring out Michonne's goofy side, then so be it. Just no more solo scenes, please. (Unless he's eating 112 ounces of chocolate pudding, because that was awesome. And Carl can't talk with his mouth full.)

Today Awww. Does little Carl want his dessert before dinner?

Daryl's adventures in babysitting

"I never" … want to see Beth again? Of all the people for Daryl to do absolutely nothing with for two whole episodes, did it really have to be the show's least interesting character? We can't agree with shippers who would've preferred to see Daryl and Carol partnered instead — "The Grove," when she reconciled with Tyreese and euthanized Lizzie "Of Mice and Men" — was one of the series' most powerful episodes. Still, imagine how much fun it would've been to see Daryl roam the countryside with someone a little ... smarter. Can you imagine the crossbow-toting redneck's reaction if he were stuck listening to Eugene chatter about video games?

Today Poor Daryl! He deserved a better (and more entertaining) companion.

Three's company

The introduction of the D.C.-bound trio of Abraham, Eugene and Rosita was a welcome sight, especially by fans who love their comic-book counterparts. It's refreshing to meet complex characters with a far-reaching agenda: to find the cause of the zombie outbreak and cure it. Their mission is serious, but their characters are fun. If we'd seen more of Eugene's mullet and less of the Governor's eye patch, this season would've been much more entertaining.



The Governator

The Governor's reinvention of himself as family man "Brian" was a fascinating character study, but it didn't need two whole episodes — "Live Bait" and "Dead Weight" — to tell it. The story of our protagonists at the prison was practically abandoned in favor of characters we either, one: despised, or two: had no emotional investment in. And now we're stuck with Tara, whose gimpy leg and guilty conscience are just dragging everybody down.

Today Didn't we see enough of the Governor last season?!

Not great, Bob

Bob Stookey, the former Army medic with a drinking problem, is one of "The Walking Dead's" more intriguing characters. We need to see more of him. And like Glenn and Maggie, his budding romance with Sasha offers another glimmer of hope in this bleak landscape. Maybe too much hope?



The claim game

For a show that prides itself on its rich, multilayered characters, Joe and his merry men are cookie-cutter criminals. And they're really damaging Daryl's calm. First Beth, then these guys? Our favorite bunny killer deserves to keep better company. Obviously we're not meant to sympathize with this group, but the story always suffers when there isn't room for empathy. (For example, the stakes were much higher when Rick clashed with the prison inmates because we felt pity for some of them.)



"The Walking Dead" is at is finest when the focus is on characters we love — or at least love to hate. Isolating them from one another this season was an interesting experiment, but — like the "searching for Sophia" narrative in season two — it went on too long. Terminus probably won't prove to be the sanctuary everyone is hoping for, but it least it means the end of their disjointed story lines.



The zombie drama does have a history of ending on brilliant notes, so in all likelihood, fans — including us — will be raving come Monday.

"The Walking Dead" season finale airs Sunday at 9 p.m. on AMC."																					1	0	0
69789	The Walking Dead's Danai Gurira To Appear On Jimmy Kimmel Live After The  ...	http://comicbook.com/blog/2014/03/30/the-walking-deads-danai-gurira-to-appear-on-jimmy-kimmel-live-after-the-season-4-finale/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:27	1		en	dead,night,gurira,live,finale,talk,season,member,kimmel,major,late,walking,jimmy,appear,deads,danai	"As The Walking Dead Season 4 wraps up this Sunday, everyone is looking for the least little bit of information which could hint at who might die during the Season 4 Finale. One idea we had to look for a clue was to look ahead at next week’s schedule for the major late night talk shows.

Our thinking was that if a major cast member was being killed off then odds are that they might be doing the talk show circuit after the show. We checked the upcoming schedules for the Tonight Show starring Jimmy Fallon, CONAN, the Late Show with David Letterman, Jimmy Kimmel Live, Arsenio Hall, the Late Late Show with Craig Ferguson, and Late Night with Seth Myers.

We could only find one Walking Dead cast member who had been booked on any of the major late night talk shows for the week after The Walking Dead Season 4 Finale. Danai Gurira is listed as appearing on Jimmy Kimmel Live on ABC on Tuesday, April 1, 2014. Interestingly enough, it was also Danai Gurira who recently went on record saying that none of the predictions about The Walking Dead Season 4 Finale were right."																					1	0	1
69790	Will 'The Walking Dead' Finale hit a New Series High? (Poll)	http://tvbythenumbers.zap2it.com/2014/03/30/will-the-walking-dead-finale-hit-a-new-series-high-poll/249108/	TVbytheNumbers	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	tvbythenumbers.zap2it.com	2014-03-31 05:59:28	1		en	series,poll,finale,bring,1849,adults,season,earned,high,walking,rating,premiere,hit,dead	"Tonight is the fourth season finale of The Walking Dead. Will the end of the “walk to Terminus” arc bring bring in the ratings?Last year’s finale earned a 6.4 adults 18-49 rating, a series high at the time. After the huge 8.2 adults 18-49 rating that the season four premiere (and midseason premiere) earned, is it even possible for the finale to set another high? Make your predictions below and tell us your reasoning (and who you think will survive!) in the comments.

Share this: Facebook

Twitter

Email

Like this: Like Loading..."																					1	0	1
69794	The Walking Dead spin-off series officially given the green light	http://www.flickeringmyth.com/2014/03/the-walking-dead-spin-off-series.html	Flickering Myth \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.flickeringmyth.com	2014-03-31 05:59:29	1		en	series,tv,developing,development,announcement,zombie,spinoff,walking,feel,amc,dead	"A new The Walking Dead spinoff TV series is in development at AMC, according to a recent announcement by the company.

The Walking Dead, AMC’s long-running zombie TV drama, already has one spinoff series in Fear the Walking Dead, as well as some films in the pipeline, but there is now going to be another spinoff series coming to the network.

We don’t have any details about what this series will be about but the announcement of the spinoff show was made during AMC Networks’ quarterly earnings call with Wall Street analysts. AMC COO Ed Carroll said (via ComicBook.com):

“We’re not at a stage where we’ll be announcing its plans to premiere. But we have hired creative people that have pitched story outlines. We feel very good about the development of that series. We’re not in a position to talk about partnerships in terms of other territories or ancillary windows, other than that there’s a healthy appetite for it and we’ve had a number of conversations with a lot of players in the space.”

Is another The Walking Dead-themed TV show something you would be interested in watching? Let us know what you would like to see from a new series in the comments below.

SEE ALSO: The Walking Dead: David Morrissey doesn’t feel finished with The Governor"																					1	0	1
69796	The Walking Dead: Andrew Lincoln Fears Norman Reedus' Wrath More Than  ...	http://comicbook.com/blog/2014/03/30/the-walking-dead-andrew-lincoln-fears-norman-reedus-wrath-more-than-death/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:29	1		en	dead,andrew,reedus,wrath,fear,yelled,prank,zombie,norman,death,walking,hes,fears,lincoln,im	"On The Walking Dead, Andrew Lincoln has been haunted by visions and phone calls from his dead wife. He believes that his infant daughter is dead, having only found a bloody car seat in the aftermath of The Governor’s attack. And we’ve lost count of how many times that he’s yelled out Carl’s name in fear that his only son is in mortal danger.

Andrew Lincoln’s character Rick Grimes has also been at death’s doorstep more than a time or two on the show. However, it’s none of those things that strike true fear into the heart of Lincoln.

During a trip to Tokyo, Lincoln helped set up a prank on Norman Reedus, where a fan with one arm and no legs crawled out of a room-service cart in zombie makeup. Lincoln revealed to the NY Post that his biggest fear is what Reedus is going to do back to him. “My big concern is that I’ve started a war. It’s on,” said Lincoln. “I’m living in fear — not that I’m gonna get killed [on the show], but I fear Norman’s wrath more than anything else. Every moment that is not a prank, he’s planning one.”"																					1	0	1
69804	The Walking Dead: The Season's Five Worst Decisions	http://comicbook.com/blog/2014/03/30/the-walking-dead-the-seasons-five-worst-decisions/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:31	1		en	governor,worst,kill,wouldnt,decisions,things,guy,rick,way,point,walking,seasons,shot,dead,ricks	"It's that old joke, right? The plucky heroine in a slasher film always runs up the stairs from the bad guy, effectively trapping herself on the second floor.Every zombie movie seems to have at least one person who, exasperated with the group's decisions, decides to go it on their own and dies almost immediately.

Basically, in order to heighten the drama and make the consequences more dire for the characters (and so more compelling/exciting for the audience), characters in a show like AMC's The Walking Dead have to do mind-numbingly stupid things that leave virtually every member of the audience at home yelling at the screen.

How did nobody shoot The Governor? Okay, so it might not have saved Hershel (and Michonne who, you've got to figure at that point, was a goner) -- but had somebody just picked off The Governor before the siege on the prison began, it would have started things out on the right foot. The fact that prior to Hershel's death, nobody was hysterically screaming and running away while they fired probably would have improved the accuracy of the potential kill shot while creating no additional threat to Rick's group of survivors. The moment the first shot escaped from Rick's Colt Python, everything unfolded exactly the way it would have if somebody had taken out The Governor beforehand, except that Rick wouldn't have been beaten to a bloody pulp by Ol' One-Eye and maybe Tara wouldn't have defected to Team Prison (although by that point it was pretty clear she was not cut out for the fight Phil was picking).

The instinct to err on the side of caution and reason is an admirable one and on some level an understandable one -- except that by this point, The Governor had already tried to kill them all, failed, succeeded in killing dozens of his own men/soldiers/friends and then somehow raised another army of a--holes try to "kill them all" a second time. Does anyone seriously believe that Rick's down-home country charm is going to be able to persuade The Governor to act like a better guy? At least taking the first shot -- even in a worst-case scenario where you don't kill the guy -- gives them a bigger priority than chopping the head off the old man, and maybe puts your "front line" of survivors by the tank in a position to make a move or escape.

Okay, so this one falls firmly into the area of My Opinion, rather than an objectively stupid decision, but since they were all standing there lamenting not having done more to put a stop to this jerk after the last time he did exactly this, I stand by it. Leaving Rick defenseless If the justification for not taking Rick on a supply run in "Claimed" is that he's too injured/in recovery to be useful, how do you then justify leaving him completely defenseless by allowing Carl to take his gun? Is there anything on the road to traveling with a knife and Michonne can't give him just as good a chance at defending himself from, as a firearm that will draw the unwanted attention of walkers if it's actually fired?

Now -- not that they know it yet, but still -- they've got a herd of semiliterate thugs after them, all angling to kill Rick for the crime of having been noticed under the bed before he killed his way out of the bathroom. And don't get us started on the fact that Rick didn't take the gun off the bed while he was making his escape, or kill Tony, who had seen his face...! Daryl and Beth burn down the house"																					1	0	1
69809	'The Walking Dead' Spin Off Series Finds Writer and Bumps Up 2015 Premiere  ...	http://www.beautyworldnews.com/articles/8461/20140328/the-walking-dead-spin-off-series-finds-writer-and-bumps-up-2015-premiere-date-as-season-4-finale-episode-approaches-amc-original-cast-safe-from-new-show-that-will-serve-as-a-horrifying-companion.htm	Beauty World News	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.beautyworldnews.com	2014-03-31 05:59:33	1		en	series,youre,spin,season,graphic,horrifying,serve,safe,forward,original,walking,amc,premiere,dead,writer	"It looks like "The Walking Dead" fans are in for a treat as the hit show based on the popular series of graphic novels has officially found a showrunner to write and produce the upcoming spin-off.

According to Hollywood Life, back in September 2013 AMC announced that the network would be moving forward with a spin off series.

Not only will the new show be receiving help from a familiar name but its premiere date has been pushed up.

This news comes just as "The Walking Dead" is nearing its season 4 finale episode.

Fans can now expect to see the spin off make its debut earlier than its initial 2015 premiere date.

Dave Erickson, who has worked as an executive producer on the show "Sons of Anarchy," will take on the same title on "The Walking Dead" spin-off.

He will also act as a co-write to the show alongside Robert Kirkman who is the original writer of "The Walking Dead" series and graphic novel.

Although details for the spin off have been kept quiet it is known that the show will serve more as a "companion" series than a true spin-off.

It won't feature any of the fan favorite characters from the AMC original series but it will tell a separate yet horrifying story.

Are you looking forward to "The Walking Dead" spinoff series? Let us you're your thoughts in the comment section below."																					1	0	1
69810	'The Walking Dead' season 4 finale spoilers: Josh McDermitt teases Terminus  ...	http://cartermatt.com/115079/walking-dead-season-4-finale-spoilers-josh-mcdermitt-teases-terminus/	CarterMatt.com	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	cartermatt.com	2014-03-31 05:59:33	1		en	updates,think,finale,thing,season,sure,theyre,ready,mcdermitt,josh,know,spoilers,walking,terminus,teases,dead,going	"







Are you ready to be completely shocked by “The Walking Dead“? We can only hope so, since the show seems to be ready and waiting to shock you. “A” is the name for the last episode, and you should also know that Terminus is involved and Rick is in big trouble thanks to the Claimers.

Luckily, one man in Josh McDermitt is ready and willing to at least give you a pretty solid set-up for the story ahead. Speaking to MTV News about both the concept of Terminus and how it plays out, the man behind Eugene raised a question as to how this could play out:

“I think people are going to be really happy with how it turns out … This group just lost the prison. They’re on railroad tracks, they’re in the woods, they’re on the road. They’re just trying to find each other. Hopefully, Terminus becomes this thing where everyone can regroup and rebuild their lives. We know Rick and Michonne and Carl are on their way there. Are we going to meet them there? What’s going to happen? I don’t know.”

What we know so far about Terminus is mostly from the comics, and the show has changed that up quite a few times already. The biggest thing that sticks in our brain right now is mostly that there is going to be a huge cliffhanger this season, arguably the biggest one to date, and we have to believe this locale will be somehow involved.

What do you think we are going to see in the finale, and do you really think that everyone who makes it to Terminus is going to live to see season 5? Share all your predictions below, and be sure to click click here in case you missed the recent news on the upcoming spin-off. You can also sign up in the event that you want more updates via our CarterMatt Newsletter.

Photo: AMC

Love TV? Be sure to like CarterMatt on Facebook for more updates!







"																					1	0	1
69811	'Walking Dead' Spinoff Update: AMC's New Zombie Drama Given The Green  ...	http://www.ibtimes.com/walking-dead-spinoff-update-amcs-new-zombie-drama-given-green-light-sons-anarchy-producer-dave	International Business Times	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.ibtimes.com	2014-03-31 05:59:34	1			dead,series,producer,work,given,drama,focus,sons,season,zombie,amc,spinoff,unique,walking,update,hurd,erickson,greenlight	"You may want to stock up on supplies and sharpen your katanas now, because a “Walking Dead” spinoff has gotten the official green light from AMC. According to TV Guide, the spinoff, which is rumored to premiere in 2015, is being led by someone who knows a thing or two about gore. Dave Erickson, known for “Sons of Anarchy,” will be joining Robert Kirkman, Gale Ann Hurd and the rest of the crew as he writes and acts as executive producer for the series.

Not too familiar with Erickson’s work? The talented writer/producer has worked on projects from “Canterbury’s Law” in 2009 to “Low Winter Sun” in 2013. Now he's trading in Harleys for flesh-eating zombies.

But according to reports, fans shouldn’t expect to see Erickson’s work too soon.

“It’s still in the very early stages because we’ve been focusing so much on ‘The Walking Dead 1.0,’” Hurd revealed to E! News at the beginning of February. “We just finished mixing the last episode of the season on Friday, so that’s been taking all of our focus, as it should.”

Charlie Collier, AMC network chief, expressed similar sentiments when he dished to Vulture that to focus energy on the spinoff before the Season 4 finale airs would be a mistake.

“What we want to do is not diminish the mothership,” Collier said in January. “What we want to do is find something that everyone involved feels as passionately about as a unique vehicle and unique enterprise as compared to the original series. We’ll take our time, and do it right.”

We just hope they don’t take too much time. We’re itching to see what “The Walking Dead” spinoff will be about. What we do know already is that the sophomore series is seeking actors. Do you think you have what it takes to fight off walkers? Find out more information about alleged casting for the new AMC series HERE!"																					1	0	1
69817	The Walking Dead: Seven Cool Things You Might Have Missed in “Us”	http://comicbook.com/blog/2014/03/26/the-walking-dead-seven-cool-things-you-might-have-missed-in-us/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:35	1		en	thats,missed,woman,things,group,weeks,daryl,season,hopeful,way,seven,painting,paintings,walking,dead,cool	"This week's episode of AMC's The Walking Dead has been the subject of a ton of conversation...

...and even more speculation about next week's season finale. Robert Kirkman and Scott Gimple had promised fans a more hopeful ending than we're used to, which was interesting. In each of the first two seasons, Rick and his group of survivors lost their "home base" at the end of the season and at the end of season three, The Governor wiped out all of his people and the prison group had to bring them all on board. While the decision to bring the Woodbury residents into the prison ultimately proved tragic when The Governor came back this year at midseason, it seemed like an awfully hopeful ending at the time.

Perhaps that's why, as the last couple of weeks have unfolded, the producers have backed away from "hopeful" a bit and promised a monster cliffhanger with major emotional impact on the characters. The paintings

We've talked about this before, but it seems as though the paintings that Carl and Michonne found while out scouting in "Claimed" are significant to the overall plot. Most of the speculation has revolved around a self-portrait painted by the woman who lived in the house. We see her in the same overalls and with the same long lock of hair, as a dessicated corpse sitting in her rocker after having mercy-killed her family and then herself. Nevertheless, the smears of blood or blood-colored paint on the painting and some basic, physical characteristics shared with Lizzie led some fans to speculate about her connection to the painting. After she passed away and the first survivors made it to Terminus, they met Mary, who also looks oddly similar to the woman in the photograph.

While Lizzie had a weird relationship with bunnies (one of the paintings in the hallway), Mary is cultivating sunflowers at Terminus (another painting). A light-colored dog like the one that came to visit Beth and Daryl, ultimately endangering them, is featured in another. It's easy to say "Oh, that's _____," but the reality is the paintings seem to be a metaphorical roadmap to the season's terrible journey. Recap for the uninitiated

Joe goes to the trouble of recapping "Claimed" from his perspective, as well; the penultimate episode of the season really felt like a fairly direct sequel to the one that we said seemed like a slasher flick, with Rick hiding out under the bed from boogeymen. He tells it all to Daryl, by way of trying to gain his trust. A man, he says, killed one of their members and left him to turn, endangering the rest of the group, when they wer eminding their own business and didn't even know he was there. From their perspective, that's true. From Rick's, they were a loud, violent group that was talking about raping women and strangling each other over sleeping arrangements. Killing one (incidentally, not as part of a plan) on the way out of the building wasn't really an undefensible act of malice -- but then again, one would assume Daryl is smart enough to know that there's some shade of gray in Joe's version of events."																					1	0	1
69818	Greg Nicotero talks 'The Walking Dead' season 4 finale spoilers, Terminus  ...	http://www.theglobaldispatch.com/greg-nicotero-talks-the-walking-dead-season-4-finale-spoilers-terminus-cannibal-rumors-87486/	The Global Dispatch	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	www.theglobaldispatch.com	2014-03-31 05:59:36	1		en	talks,finale,survive,season,nicotero,greg,doesnt,world,rick,spoilers,walking,terminus,rumors,strangle,dead	"With the finale of AMC’s The Walking Dead only a week away, fans are clamoring for news and the show’s executive producer Greg Nicotero spoke with THR in a new interview which dives into the fact surrounding Terminus and what fans can expect.

Nicotero confirms that Mary (Denise Crosby) is just the first one the group encounters at Terminus before addressing the lack of security.

“If it’s a group of people that have been posting signs all over the Georgia countryside and doing radio messages, they’re trying to rebuild the world. I’m sure that they have had to deal with good people who showed up and probably people who wanted to rob them, who knows. But you have to start somewhere, and clearly we met the “Claimers” and that situation did not end well for Len (Marcus Hester). You see that there are people out there who have their own rules.”

It’s all about surviving says Nicotero, echoing the comments by Joe (Jeff Kober).

“Clearly the Claimers survive by throwing out the rules, and we’re now getting a chance to learn about Terminus that has been able to survive and not be so creepy, weird and malevolent about it. Everyone gets to Terminus and smiles and thinks, ‘Maybe the world isn’t all a bad place.’”

Nicotero overviews the major plotpoints leading up the finale: “If Rick didn’t make that decision to strangle that guy in the house, Michonne and Carl would have been killed. So he did what he had to do, and it’s the same with Daryl… If Rick didn’t make that decision to strangle that guy in the house, Michonne and Carl would have been killed. So he did what he had to do, and it’s the same with Daryl…”

“Tyreese really lost his faith after Karen died, and reuniting with Carol and the girls, it’s amazing and gut-wrenching to see what all these people have been through. As far as Tyreese knows, Sasha is dead and vice versa. Maggie doesn’t know Beth is gone. It’s all these little microcosm of stories that will all collide.”

Nicotero doesn’t speak to Beth’s presence or doesn’t answer to questions regarding the “cannibals in the comics” only saying “That’s an interesting theory.”

Check out the full interview HERE

The Walking Dead season finale airs Sunday at 9 p.m."																					1	0	1
69819	The Walking Dead Season 4 Finale: 8 Ways It Can Avoid Sucking	http://whatculture.com/tv/walking-dead-season-4-finale-8-ways-can-avoid-sucking.php	WhatCulture\!	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	whatculture.com	2014-03-31 05:59:36	1		en	character,finale,ways,season,sucking,midseason,wander,half,good,walking,end,solid,avoid,dead	Well folks, we are almost there. Like the protagonists of AMC's Zombie drama, fans have been given a lot of time to wander toward the end of this season, completely unsure of what lies ahead. The first half of season 4 was The Walking Dead at its finest  high stakes, dramatic tension, and interpersonal drama played out much as we'd seen in the previous seasons (albeit with a more solid grasp on character motivations than the mediocre season 3). But then The Walking Dead did something you rarely see with this mid-season break  ending the first half with the requisite brutal series of murders and violence, it settled into a much more relaxed pace for the second, dividing its main cast into little groups and sending them out to wander the wilderness, all eventually heading in the general direction of "Terminus". The last seven post-prison episodes have been good, subdued character pieces, but on some level the overarching plot has suffered from a lack of focus because of the change of approach. For all its good character work and atmospheric tone, season 4 is a hard one to imagine having as thrilling a conclusion as its own mid-season finale. So, to clarify these worries, here we have a recipe to make sure that the season finale (directed by the superb Michelle MacLauren) does not waste the character building, yet provides a satisfying end to this overall quite solid season.																					1	0	1
69820	The Walking Dead: Take a Tour of Terminus	http://comicbook.com/blog/2014/03/26/the-walking-dead-take-a-tour-of-terminus/	Comicbook.com \(blog\)	e	d_i-Ey9G0TC3n_MoZU8PQo_0gpFHM	comicbook.com	2014-03-31 05:59:36	1		en	tour,bit,vent,number,undead,walking,walkers,looks,terminus,view,dead,location,dryer	"Beth

Recognizing these trials, ComicBook.com are bringing you this lovely virtual tour of Terminus, where those who arrive, survive.

Of course, if you're considering a move to Terminus, it's likely that you've got no Internet connection, so this is all a bit of a wasted effort...

Before we begin, we should credit our friends at Reddit for finding a number of different ways you can navigate safely to Terminus from your chosen location. Please be aware that there may be wreckage or walkers in the road, so driving conditions may be treacherous. Above, you can see a Google Street View of the location (although it looks a bit different after the walkers have come). Terminus, located at 795 Windsor Street Southwest in Atlanta, is a spacious location, convenient to the railroad lines and made up of a loose conglomeration of buildings that form a community where survivors of the undead apocalypse can collect. You can see a number of electric generators -- perhaps explaining where all the gasoline went that would have powered a number of cars found abandoned in a railroad garage not far from here. There are also trees and flowers, both of the fruit-bearing variety and not.

The community is easily accessible; an exterior fence is loosely chained to prevent the undead from entering, but can be easily manipulated by living humans. A closer look at the garden shows small trees, sunflowers and vegetation -- possibly corn? In any event, they're preparing to feed somebody.

This aerial view shows the scaffolding where vehicles can come up onto a ramp and enter the fenced perimeter -- presumably for loading and unloading supplies. We also see two small gardens and a hint of the urban neighborhood feel of the interior of Terminus. See? "Lower your weapons." How much more civil can you get? And just look at the flowers! More gardens inside of the grounds seem to see cabbage and cauliflower being grown.

Wait, if everyone here is all veggies, all the time, why does it smell like meat? Here we see a fire hose, fire hydrant and what looks to be a pipe for either water/sewage or perhaps just a dryer vent, with a large container (plastic? It looks a bit like canvas, which is why I thought dryer vent, but if it's plastic, it could be anything) at the bottom to catch what comes out. A number of washbins, washboards, rags and buckets. Looks like one of the creature comforts that reisdents of Terminus enjoy is definitely clean clothes...although I don't see any hanging outside. Is that a red flag -- that there aren't really that many people leaving their clothes out to dry and so perhaps newcomers found danger here and died or fled? Or is it just that it's in another place, and/or that there's a working electric dryer somewhere?"																					1	0	1
70480	Bullion market eyes e-platform to revamp London gold benchmark	http://in.reuters.com/article/2014/03/31/gold-fix-technology-idINL5N0ML3YO20140331	Reuters	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	in.reuters.com	2014-03-31 18:41:17	1		en	price,market,trading,set,fix,technology,benchmark,eplatform,bullion,bank,london,eyes,banks,gold,transparency,revamp	"* Regulatory requirements may lead to electronic solution

* Tech providers work on price discovery transparency

* Miners, refiners fear higher costs if gold fix disappears

By Clara Denina and Jan Harvey

LONDON, March 31 (Reuters) - As regulators investigate the transparency of global financial benchmarks, bullion banks are contemplating a move to electronic platforms that would shed more light on the London gold fix, a widely used reference price, sources said.

A growing number of technology providers are competing to offer a more transparent way of disseminating information that shows how the price of the $20 billion a day trade is settled.

The move was prompted by growing regulatory scrutiny after the Libor (London Interbank Offered Rate) rigging scandal exposed widespread interest-rate manipulation in 2013.

“Could the regulators say ‘we’ll let this (the daily gold settlement) carry on but only with massive transparency brought to it?’ The answer is yes, because we know the technology is being developed to do that,” a senior banking source said.

The source added that the technology would be similar to processes being developed in foreign exchange markets.

Regulators including Germany’s Bafin, Britain’s Financial Conduct Authority and the U.S. Commodity Futures Trading Commission have stepped up scrutiny of commodity indices.

The volume-matched gold benchmark is set twice a day by five banks via a teleconference, and is used widely by miners, refiners and jewellers to set their contracts.

Most gold-backed U.S. exchange-traded funds use the London afternoon gold fix to calculate their net asset value, which in turn is used by ETF custodians to calculate their fees. The U.S. Mint and Royal Canadian Mint also price their products based on daily London p.m. gold fixes, or average weekly fixes.

“Even though the gold market has undergone significant shifts in its trading mechanisms and demand behavior in the last 10 years alone, the fix is still accepted as a reference point for traders globally,” David Mazza, head of research of SPDR ETFs at State Street Global Advisors, said.

As new requirements for transparency on pre- and post-trade price discovery and trading emerge, providers say an electronic solution could improve the visibility of, for example, trading volumes during the process.

“The process itself doesn’t need changing, but a platform that broadcasts it to a wider audience could be developed,” one technology provider said.

“There is also a matter of speed on how much information can flow on stream before the price changes again or it fixes and that could also be addressed.”

Fixing members Barclays Bank, HSBC Bank USA, Societe Generale and Bank of Nova Scotia declined to comment on the matter. Deutsche Bank announced in January it was putting its seat at the fix, which it had held for 20 years, up for sale.

The Gold Fixing Company, which represents banks involved in the price settlement, is undertaking a review to ensure the gold fix is compliant with benchmark principles set by the International Organisation of Securities Commissions - a global umbrella group for markets regulators - by the July deadline, the London Bullion Market Association said in its latest Alchemist magazine issue.

Impending European EMIR (European Markets Infrastructure Regulation) and MiFID (Markets in Financial Instruments Directive) regulations will increasingly require electronically traded, centrally cleared and daily monitored transactions.

COST CONCERN

Gold miners and manufacturers are concerned they could face higher costs, should the London gold fix be abandoned under the weight of regulatory requirements and replaced with a different price mechanism, sources said.

“The fear that regulators will come out with completely exaggerated requests is so big, that people from the gold trade are afraid the other banks may even step out, like Deutsche Bank did,” a European manufacturer said.

“Then we would end up with something that is an artificial contract, very expensive.”

Many miners are active listeners to the fixing process as sellers, but they do not have to pay a commission. If they have to sell metal outside the fix, their costs may rise, they said.

“We use the fix as a benchmark when we set our contracts,” Peter Hambro, founder of Russian gold miner Petropavlovsk, said.

“(If banks withdraw from the fix) you would have to go to some sort of volume-weighted average price which is less satisfactory,” he added.

While those who use the fix say they are confident that it cannot be manipulated, the five banks involved in setting the London benchmark gold price have been accused in two recent lawsuits filed with a U.S. federal court in New York of price rigging.

“These banks work on very thin commissions and they are stuck between a rock and a hard place,” said Tony Dobra, director of trading at bullion merchant Baird & Co. (Additional reporting by Frank Tang in New York; Editing by Veronica Brown and Dale Hudson)"																					1	0	1
70488	Gold Creeps Up From 6-week Lows	http://www.rttnews.com/2294915/gold-creeps-up-from-6-week-lows.aspx\?type=cdt	RTT News	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	www.rttnews.com	2014-03-31 18:41:18	1		en	low,weekgold,yellen,economic,chicago,6week,ounce,janet,delivery,creeps,reserve,lows,gold,yellens	"Gold prices are slightly higher Monday with investors treading cautiously, choosing to wait for crucial economic data, including the U.S. jobs report for March due late in the week.

Gold futures for June delivery, moving in a very narrow range this morning, are up $1.60 or 0.12 percent at $1,295.90, not far from a six-week low of $1,285.34 hit on Friday.

Gold had settled at $1,294.30 an ounce last week, losing over 3 percent, due largely to the Federal Reserve Chief Janet Yellen's statement about a possible rise in interest rate in about a year's time and on some encouraging U.S. economic data.

Silver for May delivery is up $0.188 or 0.95 percent at $19.978 an ounce, after having declined to $19.743 an ounce earlier in the session. Silver had dropped down to a seven-week low of $19.580 an ounce last Thursday.

Meanwhile, copper is down $0.018 or 0.6 percent at $3.023 per pound.

Investors will be looking ahead to the MNI Indicators' survey on manufacturing activity in the Chicago region at 9:45 am ET. Economists expect the Chicago barometer to slip to 59 in March from 59.8 in February.

Federal Reserve Chair Janet Yellen is due to speak to the community reinvestment conference in Chicago at 9:55 am ET.

For comments and feedback contact: editorial@rttnews.com

Market Analysis"																					1	0	1
70490	Gold trades near 6-week low	http://www.resourceinvestor.com/2014/03/31/gold-trades-near-6-week-low	Resource Investor	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	www.resourceinvestor.com	2014-03-31 18:41:19	1		en	bloomberg,low,data,metal,trades,near,york,monthly,6week,ounce,fed,delivery,gold,month	"Gold traded near a six-week low in New York as investors weighed the case for the Federal Reserve to continue reducing stimulus against speculation the first monthly decline this year will increase physical demand.

Gold slipped 1.9 percent this month after U.S economic data including durable goods orders beat estimates, while Fed Chair Janet Yellen has said that the central bank’s debt-buying program may end this year with interest rates starting to rise in 2015. U.S. figures due tomorrow may show manufacturing strengthened this month.

The metal rose 70 percent from December 2008 to June 2011 as the Fed pumped more than $2 trillion into the financial system and cut interest rates to boost the economy. Gold still gained 7.8 percent this year, reaching a six-month high on March 17, as Russia’s annexation of Crimea spurred demand for a haven.

Prices have declined as “investors continued to scale back safe-haven bids and as U.S. economic data surprised to the upside,” Jonathan Butler, a precious metals strategist at Mitsubishi Corp. International (Europe) Plc in London, wrote in a report e-mailed today. “We look for the re-emergence of physical demand to keep gold reasonably well supported at these levels.”

Gold for June delivery added 0.1 percent to $1,296.10 an ounce by 7:36 a.m. on the Comex in New York. It reached $1,286.10 on March 28, the lowest since Feb. 12. Futures volume was 11 percent below the average for the past 100 days for this time of day, data compiled by Bloomberg showed. Bullion for immediate delivery was little changed at $1,295.78 in London, according to Bloomberg generic pricing.

ETP Holdings

Gold rebounded since the end of December after dropping last year by the most since 1981. Holdings in bullion-backed exchange-traded products gained 19.8 metric tons this month, set for the first back-to-back monthly expansion since December 2012, data compiled by Bloomberg show. Assets fell to 1,735.4 tons in February, the lowest since October 2009.

The Fed cut monthly asset purchases by $10 billion at the last three meetings and next meets on April 29-30. Yellen is scheduled to deliver remarks at a conference in Chicago today.

“With geopolitical tensions not escalating further, with U.S. economic data starting to come in good, and with expectations of a continuing tapering by the Fed resurfacing, people now seem to have started reducing their bullis exposure in the yellow metal,” Abhishek Chinchalkar, an analyst at Mumbai-based AnandRathi Commodities Ltd., said in a report.

Silver Prices

Silver for May delivery rose 0.9 percent to $19.965 an ounce in New York. The metal fell 6 percent in March, cutting its increase this year to 3.1 percent. Platinum for July delivery gained 1.1 percent to $1,423.30 an ounce. It declined 1.6 percent this month, the first such loss since November. Palladium for June delivery added 0.8 percent to $779.80 an ounce. Prices climbed to $802.45 on March 24, the highest since August 2011.

The metal climbed 4.7 percent this month on concern that more sanctions by the U.S. and the European Union against Russia and a strike at South African mines will reduce supplies. The countries are the largest suppliers of palladium.

U.S. Secretary of State John Kerry said Russia must pull forces back from Ukraine’s border as both sides seek a diplomatic solution. Stating they are concerned that pro-Kremlin troops massing on Ukraine’s borders may invade the ex-Soviet state, the U.S. and EU have vowed to intensify sanctions on Russia’s military, energy and financial industries.

About the Author

Copyright 2014 Bloomberg. All rights reserved. This material may not be published, broadcast, rewritten, or redistributed."																					1	0	1
70491	Gold Prices End 2-Month Rise, Chinese Buyers "Ready to Take Advantage" as  ...	http://goldnews.bullionvault.com/gold-prices-033120144	BullionVault	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	goldnews.bullionvault.com	2014-03-31 18:41:19	1			stimulus,demand,weeks,reviews,credit,import,duty,today,chinese,ounce,ready,growth,rise,end,india,gold,prices,markets	"GOLD PRICES held in a tight $6 range around last week's close at $1295 per ounce in London on Monday morning, heading for the first monthly drop of 2013 as world stock markets also held flat for the day overall.

Silver meantime spiked and fell back from $20.00, while commodities ticked down with major government bond prices.

Ten-year US Treasury yields edged higher to 2.74%, some 0.9 percentage points above their level at end-March 2013.

"We got a little ahead of ourselves on the bearish view back in January," says a note from Swiss bank and bullion market-maker Credit Suisse's precious metals analysts, noting the gold price's 17% rally from end-2013 to mid-March.

Revising Credit Suisse's end-2014 target higher to $1200 from $990 per ounce however, "We do not believe the rationale for lower gold prices ahead has changed," the note goes on, pointing to US Fed tapering and then "tightening" of interest rates.

"We do not think demand growth from Asian physical markets will be sufficient to offset supply and western investor disinterest," concludes Credit Suisse, which in January 2013 declared ' The Beginning of the End of an Era ' for rising gold prices, then at $1660.

"Despite this being a seasonally quiet time for Chinese gold demand," counters Mitsubishi analyst Jonathan Butler, "the trade is ever ready to take advantage of low prices.

"We look for the re-emergence of physical demand to keep gold reasonably well supported at these levels."

Shanghai prices for gold bullion bars today slipped again, down for the 8th time in 11 sessions even as the Chinese Yuan has slipped nearly 1% against the US Dollar.

But China's discount to benchmark London prices – most usually a premium for shipping and thanks to local demand – edged back to $3 per ounce from last week's multi-year records.

Economic growth in China – now the world's No.1 gold buyer and No.2 end-user of silver – should be maintained at a "reasonable pace", said prime minister Li Keqiang at the weekend, a comment taken by some analysts to signal possible economic stimulus ahead.

"It's difficult for the market to solely move on talk about stimulus with no concrete plan," Reuters quotes Seoul analyst Kim Yong-goo at Samsung Securities.

Eurozone stock markets were unchanged on the day after new data showed Eurozone consumer prices rising just 0.5% annually this month, the lowest rate of inflation across the 18-nation union since the deep recession of 2009.

"We believe [the ECB] are growing more concerned about growth and inflation," says Kathy Lien at New York's BK Asset Management, pointing to Thursday's monthly decision from the European Central Bank.

The issue for deciding any monetary stimulus, Lien says, is interpreting "the recent slowdown as a temporary pullback or a deeper problem."

The Euro rose on the currency markets, pushing gold prices for Eurozone investors down 0.4% from Friday's 7-week closing low to reach €938 per ounce.

Meantime in former No.1 gold buying nation India, where elections start next week, finance minister P.Chidambaram today told a news conference he's consulting with the Reserve Bank on easing the country's 10% import duty."																					1	0	1
70494	Commodities trading outlook: gold, silver and copper futures	http://www.binarytribune.com/2014/03/31/commodities-trading-outlook-gold-silver-and-copper-futures-9/	Binary Tribune	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	www.binarytribune.com	2014-03-31 18:41:20	1		en	worlds,trading,outlook,futures,metal,prices,monthly,trade,commodities,ounce,copper,silver,reserve,gold,biggest,drop	"Copper futures declined on Monday and were set for the biggest quarterly drop since the three months through June amid concern that the economy of the world’s biggest consumer of the metal is slowing, which will curb demand. Meanwhile, gold futures headed for the first monthly drop this year as further signs of recovery in the US backed the case for the Federal Reserve to keep cutting stimulus, while silver edged higher, trimming its second monthly drop since the start of the year.

On the Comex division of the New York Mercantile Exchange, copper futures for settlement in May fell by 0.46% to trade at $3.028 a pound by 13:22 GMT. Prices shifted in a daily range between $3.050, the strongest level since March 11, and $3.020 a pound. The metal settled 3.1 percent higher last week, the biggest weekly advance since the 5-day period ended August 9.

Official and private gauges of Chinese manufacturing output scheduled to be released tomorrow may indicate further signs of slowing growth in the world’s second-largest economy. The official manufacturing PMI will probably decrease to 50.1 this month, from 50.2 in February, while a report by HSBC Holdings Plc in cooperation with Markit Economics will probably be unchanged at 48.1, which signals contraction.

“Copper has more downside risks,” said Helen Lau, a commodity analyst at UOB Kay Hian Ltd. in Hong Kong, cited by Bloomberg. “The slowdown in China will continue with a crash unlikely, which will mean government stimulus will be limited”, she added.

Copper prices are 10.8% down since the beginning of the year, poised for the biggest quarterly drop since the three months through June, on concern economic growth is faltering and default risks are increasing in the world’s largest consumer, China at a time when global supplies are piling.

According to data compiled by the metals researcher CRU, the global surplus of copper may reach 140 000 tons in 2014, almost four times larger than previously estimated as demand in the biggest consumer, China, slows.

Meanwhile, on the Comex division of the New York Mercantile Exchange, gold futures for settlement in June traded little changed at $1 294.00 an ounce by 13:24 GMT, losing 0.04% for the day. Prices shifted in a daily range between $1 299.10 an ounce and $1 290.90 an ounce. On Friday, gold futures touched $1 286.40, the weakest level since February 13th.

Bullion has retreated 7.1% since reaching a six-month high of $1 392.60 an ounce on March 17 and headed for a 2.4% loss this month as the US economy expanded at a faster-than-expected pace and after Federal Reserve Chair Janet Yellen said the central bank’s bond-buying program may be brought to an end this fall, with borrowing costs starting to rise by mid-2015. The Federal Reserve trimmed its monthly bond-buying program by $10 billion at the last three meetings.

Elsewhere on the Comex, silver futures for May delivery surged by 0.72 percent to trade at $19.932 an ounce by 13:25 GMT. The precious metal, however headed for a 6.1% loss in March, registering a second monthly decline since the start of the year. Platinum futures for July delivery rose by 0.9 percent to trade at $1 419.75 an ounce. Palladium futures for June delivery surged by 0.57 percent to $758.00 an ounce. The metal has risen 8% this year on concern more sanctions by the US and the EU on Russia and a strike at South African mines may reduce supplies. The two countries are the biggest producers of palladium."																					1	0	1
70499	Gold Fundamental Analysis April 1, 2014 Forecast	http://www.fxempire.com/fundamental/fundamental-analysis-reports/gold-fundamental-analysis-april-1-2014-forecast/	FX Empire	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	www.fxempire.com	2014-03-31 18:41:21	1		en	price,likely,analysis,selloff,steep,usdjpy,yields,treasury,risk,action,fundamental,toread,technical	"Based on Monday’s price action and the early action on Tuesday, it looks as if USD/JPY investors have absorbed the plunge in U.S. Treasury yields. It further indicates the next major move in the Forex pair will likely be determined by appetite for risk. Another steep sell-off is likely to

Read More"																					1	0	1
70512	Gold futures set for first monthly drop in three months on Fed stimulus outlook	http://www.binarytribune.com/2014/03/31/gold-futures-set-for-first-monthly-drop-in-three-months-on-fed-stimulus-outlook/	Binary Tribune	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	www.binarytribune.com	2014-03-31 18:41:24	1		en	spending,set,gold,economy,rose,outlook,futures,showed,monthly,russia,ounce,fed,reserve,months,stimulus,drop	"Gold futures headed for the first monthly drop this year as further signs of recovery in the US backed the case for the Federal Reserve to keep cutting stimulus. Meanwhile, assets in the SPDR Gold Trust, the biggest bullion-backed ETF, remained unchanged on Friday.

On the Comex division of the New York Mercantile Exchange, gold futures for settlement in June traded little changed at $1 293.80 an ounce by 07:45 GMT, losing 0.04% for the day. Prices shifted in a daily range between $1 299.10 an ounce and $1 293.80 an ounce. On Friday, gold futures touched $1 286.40, the weakest level since February 13th.

Bullion has retreated 7.1% since reaching a six-month high of $1 392.60 an ounce on March 17 and headed for a 2.4% loss this month as the US economy expanded at a faster-than-expected pace and after Federal Reserve Chair Janet Yellen said the central bank’s bond-buying program may be brought to an end this fall, with borrowing costs starting to rise by mid-2015. The Federal Reserve trimmed its monthly bond-buying program by $10 billion at the last three meetings.

However, the precious metal rose 8 percent this quarter as global growth faltered and as turmoil over Ukraine left Russia and the West involved in their worst conflict since the end of the Cold War.

“Yellen alluded to a rate hike which has pressured gold lower, but investors should remember that while data is improving, the U.S. economy is still far from strong,” Sun Yonggang, a macroeconomic strategist at Everbright Futures Co., said from Shanghai, cited by Bloomberg. “While tension between Russia and Ukraine still exist, it isn’t rising for now and that’s also hurt sentiment toward gold.”

Yesterday, the US Secretary of State John Kerry told reporters in Paris after the meeting with his Russian counterpart Sergei Lavrov they have discussed that Russia must pull its military forces back from Ukraine’s border as a first step toward de-escalating the political crisis.

Fed stimulus outlook

Gold prices were pressured after data showed consumer spending in the US rose in February by the most in three months as incomes increased, adding to evidence the economy is gaining momentum after the unusually harsh winter.

Consumer spending, which accounts for almost 70% of the American economy, rose 0.3% last month, in line with analysts’ estimates and after a 0.2% increase in the previous month that was smaller than previously reported. Incomes also advanced 0.3% in February, in line with analysts’ expectations and matching January’s gain, data by the US Commerce Department showed today.

The US citizens were trying to shrug off the effects of the inclement weather as they rushed out to shop, supported by a labor market that was also gaining traction.

Also fanning negative sentiment, the US economy expanded more rapidly in the final three months of 2013 than previously estimated as consumer spending jumped by the most in three years, while initial jobless claims unexpectedly declined last week, curbing demand for the precious metal as a store of value.

The US economy expanded at a 2.6% annualized rate in the final three months of 2013, slightly below analysts’ expectations of a 2.7% gain, but up from a preliminary estimate of 2.4%, a report by the the Bureau of Economic Analysis showed yesterday. The US gross domestic product grew 4.1% in the third quarter.

Assets in the SPDR Gold Trust, the biggest bullion-backed ETP, were unchanged at 816.97 tons on Friday. Holdings in the fund are up 1% this year after it lost 41% of its assets in 2013 that wiped almost $42 billion in value. A total of 553 tons has been withdrawn last year."																					1	0	1
70522	Gold Fundamental Analysis March 28, 2014 Forecast	http://www.fxempire.com/fundamental/fundamental-analysis-reports/gold-fundamental-analysis-march-28-2014-forecast/	FX Empire	b	d_gVpCAKL5OJx5MeFYkFC0jEPlhGM	www.fxempire.com	2014-03-31 18:41:27	1		en	price,likely,analysis,selloff,steep,usdjpy,yields,treasury,risk,action,fundamental,toread,technical	"Based on Monday’s price action and the early action on Tuesday, it looks as if USD/JPY investors have absorbed the plunge in U.S. Treasury yields. It further indicates the next major move in the Forex pair will likely be determined by appetite for risk. Another steep sell-off is likely to

Read More"																					1	0	1
92162	Market Update (NASDAQ:CMCSA): Comcast makes case for Time Warner Cable  ...	http://jutiagroup.com/20140408-market-update-nasdaqcmcsa-comcast-makes-case-for-time-warner-cable-deal-to-u-s-regulators/	Jutia Group	t	d_kFzlpAiem9nGMQKPbuT9HhRMhzM	jutiagroup.com	2014-04-08 23:05:11	1		en	technical,sure,market,value,maund,stock,good,investment,zngtsxv,sees,zinc,resources,analysis	Technical analyst Clive Maund explains why he sees this zinc explorer as a good value. To be sure, Group Eleven Resources Corp.’s (ZNG:TSX.V; GRLVF:OTCQB) stock looks cheap here and good value. It is an advanced […]																					1	0	1
92187	Comcast Merger Case: Rising Competition From Online Video CMCSA VZ	http://news.investors.com/technology/040814-696308-comcast-makes-case-time-warner-merger-approval.htm	Investor's Business Daily	t	d_kFzlpAiem9nGMQKPbuT9HhRMhzM	news.investors.com	2014-04-08 23:05:18	1		en	case,restricting,rising,google,alphabetunit,follow,video,merger,competition,online,apple,internet,et,cookies,data,privacy,comcast	"Google May Follow Apple In Data Privacy Move By Limiting Web Cookies

11:40 AM ET Alphabet-unit Google could follow Apple in restricting internet cookies, a move aimed at improving consumer data privacy by impeding targeted...

11:40 AM ET Alphabet-unit Google could follow Apple in restricting internet cookies, a..."																					1	0	0
92205	Comcast Promises Faster Internet If Government OKs Deal	http://www.nationaljournal.com/tech/comcast-promises-faster-internet-if-government-oks-deal-20140408	National Journal	t	d_kFzlpAiem9nGMQKPbuT9HhRMhzM	www.nationaljournal.com	2014-04-08 23:05:23	1			faster,prices,consumers,fcc,promises,promised,merger,cable,internet,warner,deal,oks,groups,comcast	"Mil­lions of con­sumers around the coun­try will be able to stream high­er qual­ity videos and browse the Web more quickly if reg­u­lat­ors al­low Com­cast to buy Time Warner Cable, the com­pan­ies said Tues­day.

The cable pro­viders made the case for their $45.2 bil­lion mer­ger in an of­fi­cial ap­plic­a­tion to the Fed­er­al Com­mu­nic­a­tions Com­mis­sion. The Justice De­part­ment will also in­vest­ig­ate wheth­er the mer­ger of the na­tion’s top two cable com­pan­ies would vi­ol­ate fair-com­pet­i­tion laws.

In the fil­ing with the FCC, Com­cast said the ac­quis­i­tion will al­low it to up­grade Time Warner Cable’s net­work and make ad­di­tion­al in­vest­ments in its own in­fra­struc­ture. As a res­ult, many cur­rent sub­scribers of both com­pan­ies will en­joy faster In­ter­net ser­vice in the com­ing years, Com­cast prom­ised.

The pledge is likely to go over well with the Obama ad­min­is­tra­tion, which has made en­sur­ing high-speed In­ter­net ac­cess to all Amer­ic­ans a top pri­or­ity.

Com­cast said it will in­def­in­itely ex­tend In­ter­net Es­sen­tials, its low-cost broad­band In­ter­net pro­gram for low-in­come con­sumers. It also prom­ised to ex­pand the num­ber of Wi-Fi hot spots around the coun­try avail­able to its cus­tom­ers.

To re­ceive per­mis­sion to buy NBC-Uni­ver­sal in 2011, Com­cast prom­ised to fol­low the FCC’s net-neut­ral­ity rules un­til 2018. Be­cause a fed­er­al court struck down the rules earli­er this year, Com­cast is the only com­pany still bound to abide by the reg­u­la­tions, which re­quire In­ter­net pro­viders to treat all traffic equally. In its ap­plic­a­tion, Com­cast prom­ised to ex­tend that ob­lig­a­tion to Time Warner Cable areas.

Com­cast also em­phas­ized that its net­work does not cur­rently over­lap with Time Warner Cable in any mar­ket. As a res­ult, the mer­ger would not lim­it choices for any con­sumers, the com­pany ar­gued.

Com­cast said busi­nesses will likely en­joy lower prices if the deal is ap­proved, but the com­pany did not make any sim­il­ar prom­ise for home con­sumers.

Fifty pub­lic-in­terest groups quickly fired back with their own let­ter to FCC Chair­man Tom Wheel­er and At­tor­ney Gen­er­al Eric Hold­er, call­ing the mer­ger “un­think­able.”

Pub­lic Know­ledge, Free Press, Con­sumers Uni­on, and dozens of oth­er groups ar­gued that Com­cast has raised its ba­sic cable prices in re­cent years, while TWC has ac­tu­ally cut con­sumer costs. But the mer­ger is about more than just prices, the groups wrote — it’s about con­trol of the In­ter­net.

“The Com­cast-Time Warner Cable mer­ger would give Com­cast un­think­able gate­keep­er power over our com­mer­cial, so­cial and civic lives,” they wrote. “Every­one from the biggest busi­ness to the smal­lest star­tup, from elec­ted of­fi­cials to every­day people, would have to cross through Com­cast’s gates.”

Now that Com­cast has filed its of­fi­cial ap­plic­a­tion, the FCC will be­gin to in­vest­ig­ate wheth­er the deal is in the pub­lic’s in­terest. The Justice De­part­ment’s An­ti­trust Di­vi­sion will fo­cus on wheth­er the mer­ger would il­leg­ally lim­it com­pet­i­tion.

The Sen­ate Ju­di­ciary Com­mit­tee will ex­am­ine the deal at a hear­ing on Wed­nes­day fea­tur­ing testi­mony from Com­cast and Time Warner Cable ex­ec­ut­ives."																					1	0	1
92207	Comcast pitches Time Warner deals as boost to innovation	http://www.stltoday.com/business/local/comcast-pitches-time-warner-deals-as-boost-to-innovation/article_43d0c63c-886b-59c1-8de6-972b92dc3028.html	STLtoday.com	t	d_kFzlpAiem9nGMQKPbuT9HhRMhzM	www.stltoday.com	2014-04-08 23:05:23	1		en	pitches,boost,owner,warner,article,innovation,deal,comcast	You are the owner of this article.																					1	0	1
92215	Comcast, Time Warner Cable merger faces a grilling in Washington this week	http://www.washingtonpost.com/blogs/the-switch/wp/2014/04/08/comcast-time-warner-cable-merger-faces-a-grilling-in-washington-this-week/	Washington Post \(blog\)	t	d_kFzlpAiem9nGMQKPbuT9HhRMhzM	www.washingtonpost.com	2014-04-08 23:05:25	1		en	partners,technologies,websitewe,web,post,cookies,terms,thirdparty,agree,washington,data,sites	"Please enable cookies on your web browser in order to continue.

The new European data protection law requires us to inform you of the following before you use our website:

We use cookies and other technologies to customize your experience, perform analytics and deliver personalized advertising on our sites, apps and newsletters and across the Internet based on your interests. By clicking “I agree” below, you consent to the use by us and our third-party partners of cookies and data gathered from your use of our platforms. See our Privacy Policy and Third Party Partners to learn more about the use of data and your rights. You also agree to our Terms of Service."																					1	0	0
92223	Time Warner: SA news network debuting June 2	http://www.mysanantonio.com/business/local/article/Time-Warner-S-A-news-network-debuting-June-2-5383548.php	mySanAntonio.com	t	d_kFzlpAiem9nGMQKPbuT9HhRMhzM	www.mysanantonio.com	2014-04-08 23:05:28	1			network,antonio,halfhour,pearson,local,programming,weather,facility,warner,debuting,san	"Time Warner: S.A. news network debuting June 2

Michael Pearson says, “We're busy building a facility.” Michael Pearson says, “We're busy building a facility.” Photo: San Antonio Express-News Photo: San Antonio Express-News Image 1 of / 1 Caption Close Time Warner: S.A. news network debuting June 2 1 / 1 Back to Gallery

SAN ANTONIO — Time Warner Cable will launch a 24-hour local news network in San Antonio June 2 that promises subscribers live news updates, weather, sports and traffic.

Called Time Warner Cable News San Antonio, the network will provide hyper-local content, in-depth exclusives, the day's top Texas stories, weather every 10 minutes and other original programming, news director Michael Pearson said Monday.

The news channel, one of the first from Time Warner that will be in high definition, will be available exclusively to Time Warner customers throughout San Antonio. It can be seen on channels 14 and 200.

Starting Tuesday, prior to the full-launch, TWC News San Antonio will offer viewers a preview of the network's programming by airing two signature shows Monday through Friday: “Capital Tonight,” a nightly political half-hour focused on the Texas scene; and “Sports Night,” a 30-minute program with coverage of high school, college and professional sports teams in the area.

“We're busy building a facility downtown,” Pearson said, adding that TWC News San Antonio also is in the midst of hiring news and sports reporters and meteorologists.

“Production will be hubbed out to Austin (where a Time Warner news network has been based for years), but all the reporting will be local,” he added.

Initially, anchors and sportscasters will work out of Austin, he said, but eventually San Antonio will have its own setup.

The channel will be in production 20 hours a day, and content will be constantly updated. Pearson described the primary programming format as a half-hour “news wheel” that begins with a “San Antonio Minute,” followed by a brief weather forecast and local news reports. The bottom of each half-hour will contain feature stories dedicated to the San Antonio region.

jjakle@express-news.net"																					1	0	1
94063	Simon Cowell Regrets Lauren Silverman Affair	http://earsucker.com/simon-cowell-regrets-lauren-silverman-affair-30352/	earsucker	e	d_hvZDhi9quCVyMYBcebLOPzgMDdM	earsucker.com	2014-04-09 01:16:12	1		en	affair,silverman,tv,technology,spent,watching,spare,noahs,cowell,shows,movies,regrets,simon,noahnoah,lauren,fanatic	"Noah

Noah is a technology and movies fanatic. Noah's spare time is spent watching movies and TV shows."																					1	0	1
94069	Simon Cowell: I regret my Lauren Silverman affair, but the result of it steered me  ...	http://www.realitytvworld.com/news/simon-cowell-i-regret-my-lauren-silverman-affair-but-result-of-it-steered-me-from-going-down-bad-path-16183.php	Reality TV World	e	d_hvZDhi9quCVyMYBcebLOPzgMDdM	www.realitytvworld.com	2014-04-09 01:16:14	1			result,page,visit,world,bad,simon,going,follow,click,regret,silverman,steered,lauren,reality,tv,path,google,website,cowell,source	Reality TV World is now available on the all-new Google News app and website. Click here to visit our Google News page, and then click FOLLOW to add us as a news source!																					1	0	1
94095	X Factor judges 2014: Simon Cowell doesn't want a 'celebrity judge'	http://tellymix.co.uk/reality-tv/the-x-factor/180480-x-factor-judges-2014-simon-cowell-doesnt-want-a-celebrity-judge.html	Telly Mix	e	d_hvZDhi9quCVyMYBcebLOPzgMDdM	tellymix.co.uk	2014-04-09 01:16:21	1			judges,judge,previously,doesnt,jobhe,cowell,x,celebrity,actually,cheryl,ive,went,simon,factor	"X Factor 2014 boss Simon Cowell has said he doesn't want 'celebrity judges' to join him on the panel.

There are still two spots up for grabs on this year's judging line up and Simon is after someone who can actually "do the job".

He said previously of the mysterious new judges: “It would be someone who does this for a living — a manager, a songwriter. That’s my preference.”

Speaking this week, Simon went on to explain his position “There is a tendency to hire what I call ‘celebrity judges’ and, actually, what I’m looking for is someone who can really do the job.”

He added: “I’ve got to find people who actually want to do the job rather than ‘I’ve got a record coming out’. ”

The music mogul is hoping to bring back the show to its high ratings of the past, saying of his last series back in 2010: “It was just a brilliant year with Matt Cardle, Rebecca Ferguson, One Direction, Cher Lloyd. Great talent and they all went on to be successful.”

So far only Simon and Cheryl Cole have been confirmed from the panel, although Louis Walsh is widely expected to be back.

It was previously claimed that Cheryl was backing hitmakers Amanda Ghost and Sia for the spot alongside her.

Who do you want to judge on The X Factor 2014 this year? Have your say in the comments!

The X Factor airs in the autumn on ITV.

Browse pictures of some of the possible X Factor judges below..."																					1	0	1
94099	St Albans schoolboy's opening night debut as young Simon Cowell	http://www.hertsad.co.uk/what-s-on/theatre/st_albans_schoolboy_s_opening_night_debut_as_young_simon_cowell_1_3528438	Herts Advertiser	e	d_hvZDhi9quCVyMYBcebLOPzgMDdM	www.hertsad.co.uk	2014-04-09 01:16:22	1		en	debut,night,musical,cowell,schoolboys,x,talent,opening,albans,simon,young,london,st,cant	"St Albans schoolboy’s opening night debut as young Simon Cowell

LONDON, ENGLAND - MARCH 26: Producer Simon Cowell (C) poses with the cast backstage following the press night performance of "I Can't Sing! The X Factor Musical" at the London Palladium on March 26, 2014 in London, England. (Photo by David M. Benett/Getty Images) 2014 David M. Benett

Not many people can draw comparisons between themselves and Simon Cowell, let alone anyone not yet a teenager.

Share Email this article to a friend To send a link to this page you must be logged in.

But a St Albans schoolboy now has reason to compare himself to the media mogul after playing a 12-year-old version of him in new stage smash I Can’t Sing: The X Factor Musical at the London Palladium.

Fin Banks wowed a star-studded audience on the opening night of the Harry Hill-written musical, including Jennifer Saunders, Andrew Lloyd Webber and the X-Factor creator himself.

His opening number, called If That’s Not Entertainment, tells of how a young Simon plots to take over the world of entertainment with his idea for a now infamous talent show.

The fledgling star, of Verulam secondary school, said: “This is an amazing show and I can’t believe I am a part of it.

“Harry Hill is brilliant and really friendly and so are the cast.

“The show is the funniest thing I have seen.

“My opening number is pretty cool too. The audiences have loved it so far and I am really enjoying every minute.”

Warren Bacci, director of Fin’s St Albans-based talent agency Top Talent said: “The show has got fantastic reviews and we are very proud of his achievements and cannot wait to see him in it.”"																					1	0	1
95749	Stock Futures Sharply Lower; Wells Fargo Up, JPMorgan Down	http://news.investors.com/investing-stock-market-today/041114-696835-stock-futures-point-to-lower-open-friday.htm	Investor's Business Daily	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	news.investors.com	2014-04-11 15:34:16	1		en	reported,dollar,q4,line,nick,gdp,nasdaq,oil,olin,dow,week,market,slips,loss,futures,stock	"Stock futures eased lower ahead of Friday's open, as the dollar gained and Q4 GDP data came in below expectations.

Dow futures slipped 17.2 points below fair market value. S&P 500 futures were off 2.3 points. Nasdaq futures shifted from gains to a 1.5-point loss an hour before the start of regular trade.

Stock Market Today

The stock market today starts with the Nasdaq steering toward its worst week since October, down 3.2% through Thursday. The S&P 500 opens with a 2.5% loss for the week. Both indexes are testing support at their 50-day moving averages while toting a hefty count of seven distribution days each.

The Nasdaq may be gathering itself to again challenge resistance at the 5000 level. But maintaining support at the 50-day line will be the crucial test on Friday.

Economic News

The Commerce Department reported its estimate for Q4 GDP growth was 2.2%, unchanged from prior estimates, but below economist projections for an upward revision to 2.4%. The GDP price deflator inflation gauge held steady, up 0.1%, in line with expectations.

A final reading on March consumer sentiment is expected from the University of Michigan at 10 a.m. ET. Fed Chairwoman Janet Yellen is scheduled to speak in San Francisco, beginning at 3:45 p.m. ET.

Stocks

Olin (OLN) rocketed 20% higher on news that Dow Chemical (DOW) would merge its chlorine operations with Olin. The companies expect the deal, valued at $5 billion, to form an industry leader in chloralkali processing, producing vinyl, chlorinated organics and epoxy.

Dow shares rose 6% in premarket trade. Olin had pulled back below a 15-month high after briefly clearing a long-term consolidation. Dow has been consolidating since September.

Restoration Hardware (RH) slumped more than 4% ahead of the opening bell. The Corte Madera, Calif.-based chain reported late Thursday a narrow Q4 earnings beat and sales in line with expectations. Q1 guidance was below analyst targets. The stock has been forming a base-on-base cup, ending Thursday back above its 10-week line of support.

Yahoo (YHOO) added nearly 2% after its late Thursday announcement of a $2 billion share buyback initiative. The company reported the new program was in addition to the $726 million in buybacks still active under its previous plan.

Morgan Stanley launched coverage on the stock with an overweight rating and a 55 price target. Yahoo shares have been working to retake their 10-week moving average, within a four-month consolidation.

Overseas

China's markets ended relatively flat on Friday after a week that left the Shanghai Composite up 2% and Hong Kong's Hang Seng index with a 2.7% gain. Tokyo's Nikkei 225 dipped 1% on Friday to end the week little changed.

Leading indexes in Paris and Frankfurt were up nearly 1%. London's FTSE 100 showed a 0.3% loss near midday. For the week, the CAC-40 in Paris and Frankfurt's DAX were tracking toward 1% losses. The FTSE 100 traded 2.1% below last Friday's close.

Currencies/Commodities

The dollar gained on the yen and sent the euro back below 1.09. Oil pulled back, almost 2% for the U.S. benchmark West Texas Intermediate crude, to below $51, and 1% for Europe's Brent crude, to below $59."																					1	0	1
95750	Wells Fargo's earnings rise 14%	http://www.thonline.com/biztimes/articles/article_a0ab05c0-c179-11e3-9a50-001a4bcf6878.html	Dubuque Telegraph Herald	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.thonline.com	2014-04-11 15:34:16	1		en	firstquarter,rise,today,wells,earnings,biggest,14,fargos,reports,mortgage,market,fargo,opens,lender	Wells Fargo & Co., one of the biggest U.S. banks and the biggest U.S. mortgage lender, reports its first-quarter earnings before the market opens today.																					1	0	1
95763	Stock Market Today: Why JPMorgan and Wells Fargo are on the Move	http://www.fool.com/investing/general/2014/04/11/stock-market-today.aspx	Motley Fool	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.fool.com	2014-04-11 15:34:19	1		en	fool,today,trading,jpmorgan,wells,earnings,market,wall,streets,billion,premarket,fargo,revenue,mortgage,motley,stock,quarterly	"After a brutal sell-off yesterday, the Dow Jones Industrial Average (DJINDICES:^DJI) has lost 51 points in pre-market trading, suggesting a lower start to the stock market today. Global indexes followed Wall Street lower overnight: European stocks were down by more than 1% as of 7:30 a.m EDT and Japan's Nikkei index fell by 2.4%.

But earnings season is rolling on, and individual stocks on the move this morning include banking giants JPMorgan Chase (NYSE:JPM) and Wells Fargo (NYSE:WFC), which both posted quarterly results before the opening bell.

JPMorgan's earnings missed Wall Street's estimates on both the top and bottom lines. Early reaction on Twitter featured words like "terrible" from The Wall Street Journal's John Carney and "ugly" from Crossing Wall Street's Eddy Elfenbein.

Ugly seems about right. The bank's revenue came in at $23.9 billion and quarterly profit was $1.28 a share. Analysts had expected $24.5 billion in sales and per-share earnings of closer to $1.40. JPMorgan was hurt by a big drop in mortgage activity: originations fell by 68%, helping push mortgage production revenue lower by almost $1 billion. The trading business also suffered in the quarter, pulled down by a 21% fall in its fixed income products. Still, CEO Jamie Dimon sounded optimistic about the future, saying in a press release the company has "growing confidence in the economy," and that "consumers corporations and middle market companies are in increasingly good financial shape and housing has turned the corner in most markets." Investors apparently aren't sharing that optimism, as the stock was down 3.5% in pre-market trading.

Wells Fargo's numbers looked much better. The bank posted a record quarterly profit haul that powered earnings of $1.05 a share, easily beating the $0.97 that analysts had anticipated. Yes, revenue shrunk slightly to $20.6 billion, but that was in line with Wall Street's forecasts. Wells Fargo saw its mortgage business shrink as interest rates crept higher, but that dip was offset by gains elsewhere. Credit quality, for example, continued to improve for the bank, and its total deposits grew to $1.1 trillion -- up 9% from the prior year. CEO John Stumpf telegraphed more cash returns on the way for shareholders, calling it a "priority" for the bank. The stock was up 0.4% in pre-market trading."																					1	0	1
95774	Market tumble set to continue on Friday	http://marketintelligencecenter.com/articles/483263	Market Intelligence Center	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	marketintelligencecenter.com	2014-04-11 15:34:22	1		en	stocks,promotional,unsubscribe,newsletters,update,selecting,intelligence,market,receive,signing,sign,center,watch	"Sign up to receive our FREE Newsletters

* By signing up you will automatically opt in to receive the Market Intelligence Center, Morning Update, and Stocks to Watch newsletters, as well as third party promotional offers. You can unsubscribe anytime by selecting unsubscribe at the bottom of our emails. Privacy Policy"																					1	0	1
95780	Wells Fargo earns a record $5.9 billion in first quarter	http://www.charlotteobserver.com/2014/04/11/4834065/wells-fargo-earns-a-record-59.html	Charlotte Observer	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.charlotteobserver.com	2014-04-11 15:34:23	1		en	package,charlotte,million,wells,mortgage,including,sloan,fargo,waters,maxine,pay,turnaround,expects,observer,rep,tim	Wells Fargo’s awarding of a $2 million cash bonus to CEO Tim Sloan is not going over so well with the bank’s critics, including Rep. Maxine Waters, who criticized his new pay package.																					1	0	1
95781	Wells Fargo & Co. (WFC) Posts Quarterly Earnings Results, Beats Expectations  ...	http://tickerreport.com/banking-finance/184764/wells-fargo-co-wfc-posts-quarterly-earnings-results-beats-expectations-by-0-09-eps/	Ticker Report	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	tickerreport.com	2014-04-11 15:34:23	1		en	analysis,segment,credit,price,company,wells,management,banking,fargo,services,investment,loans,stock,offers	Wells Fargo & Company, a diversified financial services company, provides retail, commercial, and corporate banking services to individuals, businesses, and institutions. The company's Community Banking segment offers checking and savings accounts; credit and debit cards; and automobile, student, mortgage, home equity, and small business loans. Its Wholesale Banking segment offers commercial loans and lines of credit, letters of credit, asset-based lending, equipment leasing, international trade facilities, trade financing, collection, foreign exchange, treasury management, merchant payment processing, institutional fixed-income sales, commodity and equity risk management, corporate trust fiduciary and agency, and investment banking services, as well as online/electronic products. This segment also provides construction, and land acquisition and development loans; secured and unsecured lines of credit; interim financing arrangements; rehabilitation loans; affordable housing loans and letters of credit; loans for securitization; and real estate and mortgage brokerage services. The company's Wealth and Investment Management segment offers financial planning, private banking, credit, and investment management and fiduciary services, as well as retirement and trust services. As of February 7, 2019, it operated through 7,800 locations, 13,000 ATMs, and the Internet and mobile banking, as well as has offices in 37 countries and territories. Wells Fargo & Company was founded in 1852 and is headquartered in San Francisco, California.																					1	0	1
95787	What to Look for in JP Morgan and Wells Fargo Earnings	http://blogs.wsj.com/moneybeat/2014/04/11/what-to-look-for-in-j-p-morgan-and-wells-fargo-earnings/	Wall Street Journal \(blog\)	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	blogs.wsj.com	2014-04-11 15:34:27	1		en	sets,morning,season,wells,earnings,morgan,jp,results,set,reports,fargo,pace,watch,look	The biggest U.S. banks by assets and market capitalization kick off bank earnings season Friday morning. J.P. Morgan sets the pace when it reports at 7 a.m. ET. Wells Fargo is set announce results at 8 a.m. Here’s what to watch.																					1	0	1
95794	JPMorgan Chase's Whisper Number Lacking Confidence	http://wallstcheatsheet.com/business/jpmorgan-chases-whisper-number-lacking-confidence.html/	Wall St. Cheat Sheet	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	wallstcheatsheet.com	2014-04-11 15:34:29	1		en	confidence,chases,price,jpmorgan,lacking,earnings,company,trading,report,days,reports,movement,whisper,number	"JPMorgan Chase (NYSE:JPM) is expected to report earnings on Friday, April 11. The whisper number is $1.38, three cents behind the analysts’ estimate. Whispers range from a low of $1.45 to a high of $1.59. JPMorgan has a 75 percent positive surprise history, having topped the whisper in 36 of the 48 earnings reports for which we have data.

Earnings history:

– Beat whisper: 36 qtrs

– Met whisper: 1 qtrs

– Missed whisper: 11 qtrs

Our primary focus is on post earnings price movement. Knowing how likely a stock’s price will move following an earnings report can help you determine the best action to take (long or short). In other words, we look at what happens when the company beats or misses the whisper number expectation.

The table below indicates the average post earnings price movement within a one and thirty trading day timeframe.

The strongest price movement of -2.5 percent comes within ten trading days when the company reports earnings that beat the whisper number, and +5.3 percent within ten trading days when the company reports earnings that miss the whisper number. The overall average price move is ‘opposite’ (beat the whisper number and see weakness, miss and see strength) when the company reports earnings.

The table below indicates the most recent earnings reports and short-term price reaction.

The company has reported earnings ahead of the whisper number in three of the past four quarters with a whisper number. In the comparable quarter last year, the company reported earnings seventeen cents ahead of the whisper number. Following that report, the stock realized a 4.4 percent loss in five trading days. Last quarter, the company reported earnings twelve cents ahead of the whisper number. Following that report, the stock realized a 5.5 percent loss in ten trading days. Overall historical data indicates the company to be (on average) an ‘opposite’ price reactor when the company reports earnings.

Enter your expectation and view more earnings information here or start receiving email trade alerts by clicking here.

John Scherr is the founder and President of WhisperNumber.com, an independent financial research firm focused on earnings expectations. He is a regular contributor to CNBC and Fox Business Network, and has been featured in Barron’s, The Wall Street Journal, and MarketWatch. He is considered a leading expert on ‘whisper numbers’ and post earnings price movement analysis. WhisperNumber.com provides specific earnings trade alerts to take advantage of earnings report price movement with their Whisper Reactors subscription service.

More From Wall St. Cheat Sheet:"																					1	0	1
95798	Faulty mortgage lawsuit against Wells Fargo clears hurdles	http://www.housingwire.com/articles/29623-faulty-mortgage-lawsuit-against-wells-fargo-clears	Housing Wire	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.housingwire.com	2014-04-11 15:34:30	1		en	zavitsanos,securities,lawsuit,wells,worth,faulty,yearthis,mortgage,fargo,subprime,hurdles,clears,significant,fraud	"A lawsuit over an alleged $1.5 billion subprime mortgage-backed securities fraud scheme against Wells Fargo (WFC) and Fortis Securities cleared a significant hurdle last week when a federal judge denied the defendants extensive motions to dismiss.

European bank LBBW Luxemburg S.A.’s charges stayed on breach on contract, negligent misrepresentation and constructive fraud charges.

The lawsuit comes from a deal 2006 in which Wells Fargo sold $40 million of what it claimed to be highly rated securities to LBBW.

Sponsor Content

The securities were collateralized by subprime residential mortgages, and defaulted within a year.

This was a significant ruling in a massive fraud case where the sellers greedily squeezed money from investors despite knowing the underlying securities were riskier than represented and not even worth the price," says David Warden of the Houston-based litigation boutique Ahmad, Zavitsanos, Anaipakos, Alavi & Mensing P.C."																					1	0	1
95800	Crunching the Numbers on Bank Earnings Season: JP Morgan, Wells Fargo, Citi	http://www.thestreet.com/story/12644129/1/crunching-the-numbers-on-bank-earnings-season-jp-morgan-wells-fargo-citi.html	TheStreet.com	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.thestreet.com	2014-04-11 15:34:30	1		en	crunching,moving,21,season,value,wells,earnings,morgan,jp,citi,numbers,bank,weekly,traded,fargo,averages,levels,risky	"NEW YORK (TheStreet) -- Regional and money center banks have traded lower since the Federal Reserve reported the results of the first round of stress tests on March 21. Today I update the tables we showed in "Mega-Chart! Regional Bank Earnings Season" on April 3.

Kicking off bank earnings season are JPMorgan Chase (JPM) and Wells Fargo (WFC), which report before the opening bell on Friday.

Today's "Crunching the Numbers" tables provide updated moving averages, key levels and earnings expectations for the 24 bank stocks in the KBW Banking Index (I:BKX). See page 2 of this article for the charts.

The first table provides the five major moving averages and stochastic readings. Note that 20 of 24 of these banks are lower since March 21, led by "too big to fail" Bank of America (BAC) and Citigroup (C), which are down 5.4% and 5.8% respectively since those first stress test results. Capital One (COF) has the biggest gain but is only up 1.2%.

Note that 18 of 24 are now below their 21-day simple moving averages, which are warnings from the daily charts. Eight are below their five-week modified moving averages, which are warnings on the weekly charts.

The second table provides earnings estimates and dates, value levels at which to buy on weakness and risky levels at which to sell on strength. Since our April 3 post, analysts lowered their earnings per share estimates on seven of the 24 bank stocks, including Bank of America, Citigroup, JP Morgan and Wells Fargo, our focus names in today's report. None of the 24 had upward revisions to earnings.

This week the U.S. banking regulators decided to raise the capital leverage ratio to 5% to 6% of total assets. This will require the eight largest banks to hold another $68 billion in capital beginning in January 2018. This is in addition to a still-unknown amount that will be required to fund the Deposit Insurance Fund by September 2020.

Keep in mind that recent quarterly earnings have been buoyed by reduced reserves for losses and asset writedowns. Mortgage activities have been slashed and profitability in securities held for trading may be underwater. New mortgage issuance is at a 14-year low and first time buyers have a difficult time qualifying for loans.

One of the biggest surprises to me is that Commerce Bancshares (CBSH), Cullen Frost (CFR), US Bancorp (USB) and Wells Fargo have traded to new all-time highs when the banking index is just above its 50% Fibonacci retracement and well below its 61.8% retracement.

Bank of America ($16.62, down 5.4% since March 21) traded as high as $18.03 on March 21, then traded as low as $16.19 on April 7. It is below its 21-day and 50-day simple moving averages at $17.11 and $16.86.

The weekly chart shifts to negative with a close on Friday below its five-week modified moving average at $16.79. A semiannual value level lags at $10.69 with a quarterly pivot at $16.53 and monthly and weekly risky levels at $16.72 and $16.88.

Citigroup ($47.16, down 5.8% since March 21) has been below its 200-day SMA at $50.17 since March 26. It traded to a 2014 intraday low at $46.12 on April 8.

The weekly chart is negative, with its five-week MMA at $48.26, and with a monthly value level at $46.06. An annual value level is $21.86, with a weekly pivot at $47.21 and semiannual and quarterly risky levels at $48.06 and $49.61.

JP Morgan ($59.27, down 1.5% since March 21) set a multiyear intraday high at $61.48 on March 25, then traded as low as $58.25 on April 8 and is just below its 21-day SMA at $59.41.

The weekly chart is positive, with its five-week MMA at $58.75. Monthly and quarterly value levels are $56.06 and $54.47 with a weekly risky level at $60.85.

Wells Fargo ($49.49.10, flat since March 21) set an all-time intraday high at $50.49 on April 4, then dipped to $48.44 on April 8. The stock is above all five key moving averages shown in today's tables.

The weekly chart is positive but overbought, with its five-week MMA at $48.07. Quarterly and monthly value levels are $47.33 and $46.67, with a weekly risky level at $50.41."																					1	0	1
95806	Wells Fargo & Co. (WFC) Set to Announce Quarterly Earnings on Friday	http://tickerreport.com/banking-finance/183327/wells-fargo-co-wfc-set-to-announce-quarterly-earnings-on-friday/	Ticker Report	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	tickerreport.com	2014-04-11 15:34:32	1		en	analysis,segment,credit,price,company,wells,management,banking,fargo,services,investment,loans,stock,offers	Wells Fargo & Company, a diversified financial services company, provides retail, commercial, and corporate banking services to individuals, businesses, and institutions. The company's Community Banking segment offers checking and savings accounts; credit and debit cards; and automobile, student, mortgage, home equity, and small business loans. Its Wholesale Banking segment offers commercial loans and lines of credit, letters of credit, asset-based lending, equipment leasing, international trade facilities, trade financing, collection, foreign exchange, treasury management, merchant payment processing, institutional fixed-income sales, commodity and equity risk management, corporate trust fiduciary and agency, and investment banking services, as well as online/electronic products. This segment also provides construction, and land acquisition and development loans; secured and unsecured lines of credit; interim financing arrangements; rehabilitation loans; affordable housing loans and letters of credit; loans for securitization; and real estate and mortgage brokerage services. The company's Wealth and Investment Management segment offers financial planning, private banking, credit, and investment management and fiduciary services, as well as retirement and trust services. As of February 7, 2019, it operated through 7,800 locations, 13,000 ATMs, and the Internet and mobile banking, as well as has offices in 37 countries and territories. Wells Fargo & Company was founded in 1852 and is headquartered in San Francisco, California.																					1	0	1
95810	Guidance To Determine Upcoming Quarterly Results - Economic Highlights	http://www.nasdaq.com/article/guidance-to-determine-upcoming-quarterly-results-economic-highlights-cm342724	NASDAQ	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.nasdaq.com	2014-04-11 15:34:33	1		en	highlights,determine,q1,companies,season,growth,earnings,results,upcoming,expectations,remain,reporting,economic,quarterly,loan,guidance	"Stocks had a positive session on Tuesday after selling off in the preceding two sessions. Pre-open sentiment is indicating a modestly positive open, but the overall mood remains tentative as the market nervously awaits the Q1 earnings season.





(AA) came out with a fairly decent earnings release after the close on Tuesday, but that tells us little about to what the rest of the earnings season will bring. Including the Alcoa release, we now have 2014 Q1 results from 23 S&P 500 members. Total earnings for these 23 companies are up +14.4%, with 60.9% beating EPS expectations. Total revenues for these companies are up +6% and 43.5% are coming ahead of top-line expectations. Hard to draw any conclusions from this sample of reports, but the growth rates thus far from these companies are lower than what we saw from the same group of companies in recent quarters.The reporting cycle gets into high gear next week with almost 60 S&P 500 members reporting results, but the bank sector reporting season will get underway with results from(JPM) and(WFC) this Friday. The Zacks Consensus EPS estimate for JPM has weakened a bit in recent days while WFC's estimate has improved a bit.The overall level of Finance sector's earnings in Q1 will remain very high, but still remain below the year-earlier level. Most of earnings gains thus far have come from expense controls and reserve releases, with net interest margins still under pressure and the mortgage refinancing business steadily going down. Loan demand continues to remain to tepid, with growth barely in the low-single-digits vicinity.There is some improvement on the commercial loan side, but we have yet to see any material improvement on the consumer loan side. The consensus expectation is for the resumption of stronger loan growth later this year and beyond, with loan growth accelerating to the mid-single-digit pace in the second half of 2014 and even higher next year. This optimistic outlook, a function of above-trend growth expectations for the U.S. economy, is also expected to drive overall earnings growth in the back half of the year and beyond.Corporate guidance on the Q1 earnings calls will determine how expectations for the coming quarters will evolve. But if past is any guide, we will most likely see those estimates come down as the Q1 earnings season unfolds. All the more reason for investors to start nervous about the earnings picture."																					1	0	1
95819	WSJ: Large US Banks Seen Posting Weak Earnings	http://www.moneynews.com/companies/banks-earnings-profits-estimates/2014/04/08/id/564281/	Moneynews	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.moneynews.com	2014-04-11 15:34:35	1			stocks,weak,q1,trading,seen,earnings,bank,wells,quarter,start,report,wsj,banks,posting,journal,large	"

Editor’s Note:

Dow Predicted Will Hit 60,000 — Buy These 4 Stocks Now

Editor’s Note:

Dow Predicted Will Hit 60,000 — Buy These 4 Stocks Now

Large U.S. banks are expected to announce sluggish first-quarter profits amid weak results in trading and mortgage lending, The Wall Street Journal reports.The banks begin to report their earnings April 11, with JPMorgan Chase and Wells Fargo leading off.Of the six biggest banks, analysts forecast JPMorgan, Citigroup, Goldman Sachs and Bank of America will report lower profits for the first quarter than a year earlier, according to The Journal. They expect Morgan Stanley's earnings to be about steady.Analysts have cut their estimates for all five companies in the last six weeks, The Journal notes. Wells Fargo is seen registering a slightly higher profit than last year'.In 2013, analysts revised their earnings forecasts for the banks upward during the first quarter, helping the companies' stocks soar. The KBW Bank (stock) Index soared 35 percent last year.But the sagging expectations this year indicate bank stocks may have lost their mojo, according to The Journal."The easy money has been made on U.S. banks," William Fitzpatrick, who follows financial stocks for Manulife Asset Management, tells the paper.Meanwhile, Mark DeCambre of Quartz says banks' first-quarter woes could be a bad sign for the rest of the year."It's significant that banks are forecasting a tough start to the year, because typically financial institutions generate their strongest trading revenues in the first or second quarter," he writes."That's because large pensions, mutual funds and hedge funds make their investments at the start of the year.""																					1	0	1
95820	NY Judge Upholds Fraud Claims Against Wells Fargo, Fortis in $1.5 Billion  ...	http://www.sys-con.com/node/3050458	SYS-CON Media \(press release\)	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.sys-con.com	2014-04-11 15:34:35	1			wells,judge,read,subprime,fortis,2019,securities,technology,mortgagebacked,ny,upholds,respond,fargo,fraud,mar,kubernetes,edt,transformation,cloud,cloudexpo	"Latest Stories

BMC Named "Gold Sponsor" of CloudEXPO By Pat Romanski BMC has unmatched experience in IT management, supporting 92 of the Forbes Global 100, and earning recognition as an ITSM Gartner Magic Quadrant Leader for five years running. Our solutions offer speed, agility, and efficiency to tackle business challenges in the areas of service management, automation, operations, and the mainframe. BMC has unmatched experience in IT management, supporting 92 of the Forbes Global 100, and earning recognition as an ITSM Gartner Magic Quadrant Leader for five years running. Our solutions offer speed, agility, and efficiency to tackle business challenges in the areas of service management, automation, operations, and the mainframe. Mar. 26, 2019 09:30 AM EDT read more & respond »

CFP Deadline For CloudEXPO Silicon Valley By Yeshim Deniz At CloudEXPO Silicon Valley, June 24-26, 2019, Digital Transformation (DX) is a major focus with expanded DevOpsSUMMIT and FinTechEXPO programs within the DXWorldEXPO agenda. Successful transformation requires a laser focus on being data-driven and on using all the tools available that enable transformation if they plan to survive over the long term. A total of 88% of Fortune 500 companies from a generation ago are now out of business. Only 12% still survive. Similar percentages are found throug... At CloudEXPO Silicon Valley, June 24-26, 2019, Digital Transformation (DX) is a major focus with expanded DevOpsSUMMIT and FinTechEXPO programs within the DXWorldEXPO agenda. Successful transformation requires a laser focus on being data-driven and on using all the tools available that enable transformation if they plan to survive over the long term. A total of 88% of Fortune 500 companies from a generation ago are now out of business. Only 12% still survive. Similar percentages are found throug... Mar. 26, 2019 05:00 AM EDT read more & respond »

DevOpsSUMMIT Named Top DevOps Influencer in the World By Zakia Bouachraoui The graph represents a network of 1,329 Twitter users whose recent tweets contained "#DevOps", or who were replied to or mentioned in those tweets, taken from a data set limited to a maximum of 18,000 tweets. The network was obtained from Twitter on Thursday, 10 January 2019 at 23:50 UTC. The tweets in the network were tweeted over the 7-hour, 6-minute period from Thursday, 10 January 2019 at 16:29 UTC to Thursday, 10 January 2019 at 23:36 UTC. Additional tweets that were mentioned in this... The graph represents a network of 1,329 Twitter users whose recent tweets contained "#DevOps", or who were replied to or mentioned in those tweets, taken from a data set limited to a maximum of 18,000 tweets. The network was obtained from Twitter on Thursday, 10 January 2019 at 23:50 UTC. The tweets in the network were tweeted over the 7-hour, 6-minute period from Thursday, 10 January 2019 at 16:29 UTC to Thursday, 10 January 2019 at 23:36 UTC. Additional tweets that were mentioned in this... Mar. 26, 2019 12:00 AM EDT read more & respond »

Cloud-Native: A New Ecosystem for Putting Containers into Production By Yeshim Deniz The standardization of container runtimes and images has sparked the creation of an almost overwhelming number of new open source projects that build on and otherwise work with these specifications. Of course, there's Kubernetes, which orchestrates and manages collections of containers. It was one of the first and best-known examples of projects that make containers truly useful for production use. However, more recently, the container ecosystem has truly exploded. A service mesh like Istio a... The standardization of container runtimes and images has sparked the creation of an almost overwhelming number of new open source projects that build on and otherwise work with these specifications. Of course, there's Kubernetes, which orchestrates and manages collections of containers. It was one of the first and best-known examples of projects that make containers truly useful for production use. However, more recently, the container ecosystem has truly exploded. A service mesh like Istio a... Mar. 25, 2019 07:15 PM EDT read more & respond »

Puppet to Present at DevOpsSUMMIT Silicon Valley By Yeshim Deniz Technology has changed tremendously in the last 20 years. From onion architectures to APIs to microservices to cloud and containers, the technology artifacts shipped by teams has changed. And that's not all - roles have changed too. Functional silos have been replaced by cross-functional teams, the skill sets people need to have has been redefined and the tools and approaches for how software is developed and delivered has transformed. When we move from highly defined rigid roles and systems to ... Technology has changed tremendously in the last 20 years. From onion architectures to APIs to microservices to cloud and containers, the technology artifacts shipped by teams has changed. And that's not all - roles have changed too. Functional silos have been replaced by cross-functional teams, the skill sets people need to have has been redefined and the tools and approaches for how software is developed and delivered has transformed. When we move from highly defined rigid roles and systems to ... Mar. 25, 2019 06:45 PM EDT read more & respond »

CloudBlue to Exhibit at CloudEXPO Silicon Valley By Liz McMillan After years of investments and acquisitions, CloudBlue was created with the goal of building the world's only hyperscale digital platform with an increasingly infinite ecosystem and proven go-to-market services. The result? An unmatched platform that helps customers streamline cloud operations, save time and money, and revolutionize their businesses overnight. Today, the platform operates in more than 45 countries and powers more than 200 of the world's largest cloud marketplaces, managing mo... After years of investments and acquisitions, CloudBlue was created with the goal of building the world's only hyperscale digital platform with an increasingly infinite ecosystem and proven go-to-market services. The result? An unmatched platform that helps customers streamline cloud operations, save time and money, and revolutionize their businesses overnight. Today, the platform operates in more than 45 countries and powers more than 200 of the world's largest cloud marketplaces, managing mo... Mar. 25, 2019 06:15 PM EDT read more & respond »

Cloud Native Programming with Docker, Kubernetes, and Ballerina By Zakia Bouachraoui Docker and Kubernetes are key elements of modern cloud native deployment automations. After building your microservices, common practice is to create docker images and create YAML files to automate the deployment with Docker and Kubernetes. Writing these YAMLs, Dockerfile descriptors are really painful and error prone.Ballerina is a new cloud-native programing language which understands the architecture around it - the compiler is environment aware of microservices directly deployable into infra... Docker and Kubernetes are key elements of modern cloud native deployment automations. After building your microservices, common practice is to create docker images and create YAML files to automate the deployment with Docker and Kubernetes. Writing these YAMLs, Dockerfile descriptors are really painful and error prone.Ballerina is a new cloud-native programing language which understands the architecture around it - the compiler is environment aware of microservices directly deployable into infra... Mar. 25, 2019 04:00 PM EDT read more & respond »

Server less Sponsorship Opportunities at DevOpsSUMMIT Silicon Valley By Zakia Bouachraoui The widespread success of cloud computing is driving the DevOps revolution in enterprise IT. Now as never before, development teams must communicate and collaborate in a dynamic, 24/7/365 environment. There is no time to wait for long development cycles that produce software that is obsolete at launch. DevOps may be disruptive, but it is essential. DevOpsSUMMIT at CloudEXPO expands the DevOps community, enable a wide sharing of knowledge, and educate delegates and technology providers alike. The widespread success of cloud computing is driving the DevOps revolution in enterprise IT. Now as never before, development teams must communicate and collaborate in a dynamic, 24/7/365 environment. There is no time to wait for long development cycles that produce software that is obsolete at launch. DevOps may be disruptive, but it is essential. DevOpsSUMMIT at CloudEXPO expands the DevOps community, enable a wide sharing of knowledge, and educate delegates and technology providers alike. Mar. 25, 2019 03:30 PM EDT read more & respond »

Singtel to Exhibit at @CloudEXPO Silicon Valley By Elizabeth White The platform combines the strengths of Singtel's extensive, intelligent network capabilities with Microsoft's cloud expertise to create a unique solution that sets new standards for IoT applications," said Mr Diomedes Kastanis, Head of IoT at Singtel. "Our solution provides speed, transparency and flexibility, paving the way for a more pervasive use of IoT to accelerate enterprises' digitalisation efforts. AI-powered intelligent connectivity over Microsoft Azure will be the fastest connected pat... The platform combines the strengths of Singtel's extensive, intelligent network capabilities with Microsoft's cloud expertise to create a unique solution that sets new standards for IoT applications," said Mr Diomedes Kastanis, Head of IoT at Singtel. "Our solution provides speed, transparency and flexibility, paving the way for a more pervasive use of IoT to accelerate enterprises' digitalisation efforts. AI-powered intelligent connectivity over Microsoft Azure will be the fastest connected pat... Mar. 25, 2019 02:00 PM EDT read more & respond »

Apptio Named "Bronze Sponsor" of CloudEXPO By Liz McMillan Apptio fuels digital business transformation. Technology leaders use Apptio's machine learning to analyze and plan their technology spend so they can invest in products that increase the speed of business and deliver innovation. With Apptio, they translate raw costs, utilization, and billing data into business-centric views that help their organization optimize spending, plan strategically, and drive digital strategy that funds growth of the business. Technology leaders can gather instant recomm... Apptio fuels digital business transformation. Technology leaders use Apptio's machine learning to analyze and plan their technology spend so they can invest in products that increase the speed of business and deliver innovation. With Apptio, they translate raw costs, utilization, and billing data into business-centric views that help their organization optimize spending, plan strategically, and drive digital strategy that funds growth of the business. Technology leaders can gather instant recomm... Mar. 25, 2019 01:00 PM EDT read more & respond »

Sponsorship and Speaking Opportunities at CloudEXPO Silicon Valley By Zakia Bouachraoui At CloudEXPO Silicon Valley, June 24-26, 2019, Digital Transformation (DX) is a major focus with expanded DevOpsSUMMIT and FinTechEXPO programs within the DXWorldEXPO agenda. Successful transformation requires a laser focus on being data-driven and on using all the tools available that enable transformation if they plan to survive over the long term. A total of 88% of Fortune 500 companies from a generation ago are now out of business. Only 12% still survive. Similar percentages are found throug... At CloudEXPO Silicon Valley, June 24-26, 2019, Digital Transformation (DX) is a major focus with expanded DevOpsSUMMIT and FinTechEXPO programs within the DXWorldEXPO agenda. Successful transformation requires a laser focus on being data-driven and on using all the tools available that enable transformation if they plan to survive over the long term. A total of 88% of Fortune 500 companies from a generation ago are now out of business. Only 12% still survive. Similar percentages are found throug... Mar. 25, 2019 12:30 PM EDT read more & respond »

Nutanix for DevOps: Agility from Technology By Yeshim Deniz In today's always-on world, customer expectations have changed. Competitive differentiation is delivered through rapid software innovations, the ability to respond to issues quickly and by releasing high-quality code with minimal interruptions. DevOps isn't some far off goal; it's methodologies and practices are a response to this demand. The demand to go faster. The demand for more uptime. The demand to innovate. In this keynote, we will cover the Nutanix Developer Stack. Built from the foundat... In today's always-on world, customer expectations have changed. Competitive differentiation is delivered through rapid software innovations, the ability to respond to issues quickly and by releasing high-quality code with minimal interruptions. DevOps isn't some far off goal; it's methodologies and practices are a response to this demand. The demand to go faster. The demand for more uptime. The demand to innovate. In this keynote, we will cover the Nutanix Developer Stack. Built from the foundat... Mar. 25, 2019 12:00 PM EDT read more & respond »

Rockstar Kubernetes Faculty at CloudEXPO Announced By Roger Strukhoff As you know, enterprise IT conversation over the past year have often centered upon the open-source Kubernetes container orchestration system. In fact, Kubernetes has emerged as the key technology -- and even primary platform -- of cloud migrations for a wide variety of organizations. Kubernetes is critical to forward-looking enterprises that continue to push their IT infrastructures toward maximum functionality, scalability, and flexibility. As they do so, IT professionals are also embr... As you know, enterprise IT conversation over the past year have often centered upon the open-source Kubernetes container orchestration system. In fact, Kubernetes has emerged as the key technology -- and even primary platform -- of cloud migrations for a wide variety of organizations. Kubernetes is critical to forward-looking enterprises that continue to push their IT infrastructures toward maximum functionality, scalability, and flexibility. As they do so, IT professionals are also embr... Mar. 25, 2019 12:00 PM EDT read more & respond »

Sponsorship and Speaking Opportunities at CloudEXPO Silicon Valley By Zakia Bouachraoui CloudEXPO has been the M&A capital for Cloud companies for more than a decade with memorable acquisition news stories which came out of CloudEXPO expo floor. DevOpsSUMMIT New York faculty member Greg Bledsoe shared his views on IBM's Red Hat acquisition live from NASDAQ floor. Acquisition news was announced during CloudEXPO New York which took place November 12-13, 2019 in New York City. CloudEXPO has been the M&A capital for Cloud companies for more than a decade with memorable acquisition news stories which came out of CloudEXPO expo floor. DevOpsSUMMIT New York faculty member Greg Bledsoe shared his views on IBM's Red Hat acquisition live from NASDAQ floor. Acquisition news was announced during CloudEXPO New York which took place November 12-13, 2019 in New York City. Mar. 25, 2019 11:00 AM EDT read more & respond »"																					1	0	1
95830	Baird Adds Wells Fargo Advisor, Reports '13 Results	http://www.thinkadvisor.com/2014/04/07/baird-adds-wells-fargo-advisor-reports-13-results	ThinkAdvisor	b	d_d9JuRRu0Fhw0MNMIcAYdv3EZzaM	www.thinkadvisor.com	2014-04-11 15:34:38	1		en	charleston,baird,adds,wells,results,reports,financial,manager,fargo,jr,jody,clients,13,advisor,branch,wealth	"Joseph “Jody” H. McAuley Jr. has joined Baird's office in Charleston, S.C.

Robert W. Baird said Monday it recruited a new branch manager in Charleston, S.C., from Wells Fargo (WFC). The employee-owned company also posted its 2013 financial results and noted that it recruited 44 veteran advisors and branch managers last year.

Milwaukee-based Baird now has more than 725 financial advisors serving clients nationwide in 75 offices. It’s picked up more than 325 reps since 2009.

“Baird’s record financial results and the milestones we surpassed in 2013 are the result of client-focused, strategic initiatives over a number of years to consistently expand our capabilities in each of our businesses,” said Chairman and CEO Paul E. Purcell, in a press release. “Our strong performance is meaningful to us because it reflects the trust our clients place in us to provide them with expert advice that is in their best interests.”

The firm’s overall revenues were $1.1 billion in 2013 vs. $961 million in 2012. Operating income totaled $117 million, up 17% from a year ago, and the firm’s 2013 return on equity rose to more than 15%. Client asset grew to more than $117 billion by year end.

Latest Recruit

Baird says Joseph “Jody” H. McAuley Jr. is now a branch manager and producing advisor at its Charleston, S.C., wealth management office.

Charles “Bucky” W. Knowlton Jr., the previous branch manager, will continue to serve clients and grow his advisor business, the group adds.

“With more than 15 years of industry experience in the Carolinas, his proven leadership ability and a strong commitment to excellent client service, Jody is well-positioned to manage our Charleston office,” said Bill Johnson, regional director for Baird’s Private Wealth Management group, in a statement.

McAuley began his career in the financial industry in 1997 with the former A.G. Edwards & Sons and remained there through mergers with Wachovia Securities and Wells Fargo before joining Baird."																					1	0	1
110903	Food Guide to Coney Island	http://www.thedailymeal.com/food-guide-coney-island	The Daily Meal	e	d_FAribUN4t2AiMGCWLN7FpUdZzLM	www.thedailymeal.com	2014-04-14 09:07:19	1		en	shop,island,york,coney,egg,famous,food,cream,pizza,guide,brooklyn,totonnos	"At the southern end of Brooklyn, Coney Island is a summertime treat for New Yorkers. It's amusement park, Luna Park, re-opened this weekend for the season. To herald the opening of the rides, carnival games, and food stalls, the 87-year-old Cyclone was doused with a classic New York egg cream on the morning of April 13.

The iconic soda-fountain drink is made with milk, seltzer, and, traditionally, Fox’s U-Bet chocolate syrup.

See New York City's Top 10 Egg Creams (Slideshow)

While there aren't too many spots to actually buy an egg cream at Coney Island, there are several dining options among the stalls selling pastel-hued cotton candy, salty popcorn, and sweet funnel cakes.

Start at Totonno's just off the boardwalk on Neptune Ave. By all accounts, Totonno’s shouldn’t be around anymore. Consider first that it was opened in Coney Island in 1924 (by Antonio "Totonno" Pero, a Lombardi’s alum). Then factor in the fire that broke out in the coal storage area and ravaged the place in 2009. Add to that insult the destruction (and some reported $150,000 in repairs) incurred in 2012 during Hurricane Sandy when four feet of water destroyed everything inside the family-owned institution. You’ll probably agree that Brooklyn (and the country) should be counting its lucky stars Totonno’s is still around. And yet it does more than that.

It doesn’t just keep a storied pizza name, or nostalgia for simpler times (and perhaps more authentic and consistent pies) alive. No. Owners Antoinette Balzano, Frank Balzano, and Louise "Cookie" Ciminieri don’t just bridge our modern era’s festishizing of pizza to the days of its inception at Lombardi’s. The coal-fired blistered edges, the spotty mozzarella laced over that beautiful red sauce… ah, fuggedabout all the teary-eyed try-too-much words, this is Neptune Avenue! This is Brooklyn! This is Totonno’s. And this, is how you make pizza and land at #12 on The Daily Meal's 101 Best Pizzas in America.

A stroll along the beach's boardwalk is a must. A recent addition is Coney's Cones ice cream shop. The shop churns homemade traditional flavors like chocolate, vanilla, and strawberry but more daring flavors like bacon and has served more than 100,000 scoops since opening in 2011.

Just as famous as the Cyclone roller coaster, perhaps, is the annual Nathan's Famous Hot-Dog Eating Contest held on the July 4th at the intersection of Surf and Stillwell Ave., where Nathan’s Famous Hot Dogs has been in business since 1916. Stop by to have one of the chain's famous frankfurters.

If you haven't had enough of a sugar rush, get some to go at the whimsical IT'SUGAR. The name says it all at this saccharine shop that specializes in gigantic, life-size candy and sweets. Cereal-box size boxes of Nerds, one pound Snickers bars, and lollipops the size of Frisbees ensure you'll never run out of sweets. Opened in 2006 by Jeff Rubin, IT'SUGAR has 70 locations around the world, including New York which has shops from Coney Island to Lincoln Center.

Lauren Mack is The Daily Meal's New York City Travel Editor. Follow her on Twitter @lmack."																					1	0	0
110904	Luna Park opens for the season to crowds seeking thrills at the Coney Island  ...	http://www.nydailynews.com/new-york/brooklyn/luna-park-official-opening-draws-crowds-article-1.1755281	New York Daily News	e	d_FAribUN4t2AiMGCWLN7FpUdZzLM	www.nydailynews.com	2014-04-14 09:07:20	1		en	island,ice,crowds,coney,season,enjoy,luna,thrills,great,park,amusement,opens,seeking,able	"After all the ice all year, it's great to be able to enjoy this," he said.																					1	0	1
126870	Tori Spelling Hurt Over Weight Loss Reports	http://earsucker.com/tori-spelling-hurt-weight-loss-reports-73663/	earsucker	e	d_hP3EGsDXIs-CM5xZ9FoZSE3oPqM	earsucker.com	2014-04-17 07:49:34	1		en	simon,cowell,elimination,episode,mean,reports,hurt,factors,spelling,tori,demi,lovato,x,weight,loss	Simon Cowell Mean To Demi Lovato On The X Factor’s Elimination Episode?																					1	0	1
126911	Tori Spelling Speaks for First Time About Unfaithful Husband Dean McDermott	http://www.justjared.com/2014/04/16/tori-spelling-speaks-for-first-time-about-unfaithful-husband-dean-mcdermott/	Just Jared	e	d_hP3EGsDXIs-CM5xZ9FoZSE3oPqM	www.justjared.com	2014-04-17 07:49:45	1		en	taking,speaks,store,zendaya,husband,unfaithful,priyanka,wife,mcdermott,dean,jonas,spelling,tori,video,chopra,nick,visits	"Nick Jonas' Wife Priyanka Chopra Visits His Music Video... Nick Jonas holds hands with wife Priyanka Chopra while taking a break from filming his new Jonas...

Zendaya Was Not Prepared for This Paparazzi Moment, But... Zendaya chats on her phone while leaving a store on Tuesday afternoon (March 26) in Los Angeles...."																					1	0	1
126916	Friends worry Tori Spelling is doing 'True Tori' show to exact revenge on Dean  ...	http://starcasm.net/archives/268877	Starcasm.net	e	d_hP3EGsDXIs-CM5xZ9FoZSE3oPqM	starcasm.net	2014-04-17 07:49:46	1		en	friends,closed,account,exact,sure,recovered,deleted,permanently,data,mcdermott,dean,spelling,tori,true,doing,revenge,worry	Your account will be closed and all data will be permanently deleted and cannot be recovered. Are you sure?																					1	0	1
126922	Tori Spelling Spends Quality Time with Kids Amid Marriage Woes	http://www.toofab.com/2014/04/15/tori-spelling-kids-photos/	TooFab.com	e	d_hP3EGsDXIs-CM5xZ9FoZSE3oPqM	www.toofab.com	2014-04-17 07:49:47	1		en	woes,marriage,blue,looks,youngest,woescheck,white,quality,easter,spends,spelling,tori,kids,amid,yellow,yearold,purple	It looks like Tori’s getting in the Easter spirit!spent some quality time with her cute kids on Monday, sipping iced tea and dying Easter eggs.While listening to music from a purple iHome boom box , the mother-of-four chaperoned as her three youngest children carefully coated the eggs in pink, purple, yellow, orange, and blue dyes.The actress’ one year-old son,, seemed to make a bit of a mess, spilling dots of blue dye on his red and white striped shirt!Following the recent drama surrounding Tori and her hubbytroubled marriage, it looks like the formerstar is putting her kids first as she bonds with her brood over Easter activities.The first trailer for her new reality show,was recently released -- and it looks like the show is going to give viewers an unflinching look at the couple's marital woes.Check out the clip below to see what's in store for the upcoming season. Will you tune in? Sound off!																					1	0	1
149542	JUNIPER NETWORKS	http://news.investors.com/042214-697997-juniper-networks.htm	Investor's Business Daily	b	d_CswVIPiQ_gM5M9wJF8Gi1oa57aM	news.investors.com	2014-04-23 04:29:30	1		en	breakout,networks,falls,rides,stock,tech,downgrade,wellpositioned,technical,jefferies,juniper,stocks,showing,arista	"This Leader Among Tech Stocks Rides Current Stock Market Higher

3/13/2019 Arista Networks was among the tech stocks to breakout Wednesday, with technical gauges showing the stock well-positioned in the current...

3/13/2019 Arista Networks was among the tech stocks to breakout Wednesday,..."																					1	0	1
149543	Juniper Networks (JNPR) Releases Quarterly Earnings Results	http://www.mideasttime.com/juniper-networks-jnpr-releases-quarterly-earnings-results/122311/	Mideast Time	b	d_CswVIPiQ_gM5M9wJF8Gi1oa57aM	www.mideasttime.com	2014-04-23 04:29:30	1		en	networks,provides,company,stock,analysis,routers,platform,offers,cloud,series,juniper,services,price,products,data	Juniper Networks, Inc. designs, develops, and sells network products and services worldwide. The company offers various routing products, such as ACX series universal access routers to deploy new high-bandwidth services; MX series Ethernet routers that functions as a universal edge platform; PTX series packet transport routers; cloud customer premises equipment; and NorthStar controllers. It also provides switching products, including EX series Ethernet switches to address the access, aggregation, and core layer switching requirements of micro branch, branch office, and campus and data center environments; and QFX series of core, spine, and top-of-rack data center switches. In addition, the company offers security products comprising SRX series services gateways for the data centers; Branch SRX family provides integrated firewall capabilities; vSRX Virtual Firewall that delivers various features of physical firewalls; and Sky Advanced Threat Prevention, a cloud-based service for static and dynamic analysis. Further, it offers Junos OS, a network operating system; Contrail networking and cloud platform, which provides an open-source and standards-based platform for SDN and NFV; and AppFormix, an optimization and management software platform for public, private, and hybrid clouds. Additionally, the company provides technical support, maintenance, and professional services, as well as education and training programs. It sells its products through direct sales, distributors, value-added resellers, and original equipment manufacturer partners to end-users in the cloud, telecom/cable, and strategic enterprise markets. Juniper Networks, Inc. was founded in 1996 and is headquartered in Sunnyvale, California.																					1	0	1
149552	Juniper Networks Inc.: Juniper Networks Reports Preliminary First Quarter 2014  ...	http://www.twst.com/update/53113-juniper-networks-inc-juniper-networks-reports-preliminary-first-quarter-2014-financial-results	The Wall Street Transcript	b	d_CswVIPiQ_gM5M9wJF8Gi1oa57aM	www.twst.com	2014-04-23 04:29:32	1		en	networks,quarter,operating,net,reports,results,cash,financial,income,nongaap,juniper,preliminary,compensation	"04/22/2014

Top Company Interviews



Revenue: $1,170 million, down 8% from Q4'13 and up 10% from Q1'13

Operating Margin: (0.5)% GAAP, includes $122 million of restructuring and other charges; 17.2% non-GAAP, up 1.5 pts from Q1'13

GAAP Net Income Per Share: $0.22 diluted, includes a $0.33 gain from the sale of minority equity investments and a $0.25 impact from restructuring and other charges

Non-GAAP Net Income Per Share: $0.29 diluted, down from $0.43 diluted in Q4'13 and up from $0.24 diluted in Q1'13

Revenues will be in the range of $1,200 million to $1,230 million.





Non-GAAP gross margin will be approximately 64.0%, plus or minus 0.5%.





Non-GAAP operating expenses will be $520 million, plus or minus $5 million.





Non-GAAP operating margin will be roughly 21.0%, plus or minus 0.5% at the midpoint of revenue guidance.





Non-GAAP net income per share will range between $0.36 and $0.39 on a diluted basis. This assumes a share count of 480 million and a non-GAAP tax rate flat to the first quarter.





Juniper Networks, Inc. Preliminary Condensed Consolidated Statements of Operations (in millions, except per share amounts) (unaudited) Three Months Ended March 31, 2014 2013 -------------- -------------- Net revenues: Product $ 876.0 $ 781.8 Service 294.1 277.4 -------------- -------------- Total net revenues 1,170.1 1,059.2 Cost of revenues: Product 326.6 278.2 Service 123.4 110.2 -------------- -------------- Total cost of revenues 450.0 388.4 -------------- -------------- Gross margin 720.1 670.8 Operating expenses: Research and development 264.0 262.2 Sales and marketing 273.4 256.1 General and administrative 74.9 58.5 Restructuring and other charges 114.0 7.0 -------------- -------------- Total operating expenses 726.3 583.8 -------------- -------------- Operating (loss) income (6.2) 87.0 Other income (expense), net 154.2 (10.1) -------------- -------------- Income before income taxes 148.0 76.9 Income tax provision (benefit) 37.4 (14.1) -------------- -------------- Net income $ 110.6 $ 91.0 ============== ============== Net income per share: Basic $ 0.23 $ 0.18 ============== ============== Diluted $ 0.22 $ 0.18 ============== ============== Shares used in computing net income per share: Basic 486.2 504.7 ============== ============== Diluted 496.5 512.7 ============== ============== Juniper Networks, Inc. Preliminary Net Revenues by Product and Service (in millions) (unaudited) Three Months Ended March 31, 2014 2013 -------------- -------------- Routing $ 549.8 $ 513.6 Switching 192.0 131.5 Security 134.2 136.7 -------------- -------------- Total product 876.0 781.8 Total service 294.1 277.4 -------------- -------------- Total $ 1,170.1 $ 1,059.2 ============== ============== Juniper Networks, Inc. Preliminary Net Revenues by Geographic Region (in millions) (unaudited) Three Months Ended March 31, 2014 2013 -------------- -------------- Americas $ 681.5 $ 592.1 Europe, Middle East, and Africa 295.7 290.6 Asia Pacific 192.9 176.5 -------------- -------------- Total $ 1,170.1 $ 1,059.2 ============== ============== Juniper Networks, Inc. Preliminary Net Revenues by Market (in millions) (unaudited) Three Months Ended March 31, 2014 2013 -------------- -------------- Service Provider $ 782.7 $ 712.9 Enterprise 387.4 346.3 -------------- -------------- Total $ 1,170.1 $ 1,059.2 ============== ============== Juniper Networks, Inc. Reconciliation between GAAP and non-GAAP Financial Measures (in millions, except percentages and per share amounts) (unaudited) Three Months Ended March 31, December 31, March 31, 2014 2013 2013 ----------- -------------- ----------- GAAP operating (loss) income $ (6.2) $ 195.4 $ 87.0 GAAP operating margin (0.5)% 15.3% 8.2% Share-based compensation expense C 60.8 63.9 49.9 Share-based payroll tax expense C 7.0 0.6 3.5 Amortization of purchased intangible assets A 9.5 9.1 7.5 Restructuring and other charges B 122.4 18.9 7.7 Acquisition-related charges A 0.6 0.7 0.1 Litigation charge B -- (10.3) 10.3 Non-routine stockholder activities B 7.3 -- -- ----------- -------------- ----------- Non-GAAP operating income $ 201.4 $ 278.3 $ 166.0 Non-GAAP operating margin 17.2% 21.9% 15.7% =========== ============== =========== GAAP net income $ 110.6 $ 151.8 $ 91.0 Share-based compensation expense C 60.8 63.9 49.9 Share-based payroll tax expense C 7.0 0.6 3.5 Amortization of purchased intangible assets A 9.5 9.1 7.5 Restructuring and other charges B 122.4 18.9 7.7 Acquisition-related charges A 0.6 0.7 0.1 Litigation charge B -- (10.3) 10.3 Non-routine stockholder activities B 7.3 -- -- Gain on equity investments B (164.0) (2.4) (1.6) Income tax effect of non-GAAP exclusions B (11.6) (16.5) (44.6) ----------- -------------- ----------- Non-GAAP net income $ 142.6 $ 215.8 $ 123.8 ----------- -------------- ----------- GAAP diluted net income per share $ 0.22 $ 0.30 $ 0.18 ----------- -------------- ----------- Non-GAAP diluted net income per share D $ 0.29 $ 0.43 $ 0.24 ----------- -------------- ----------- Shares used in computing diluted net income per share 496.5 505.6 512.7 =========== ============== ===========

Juniper Networks, Inc. Preliminary Condensed Consolidated Balance Sheets (in millions) (unaudited) March 31, December 31, 2014 2013 -------------- -------------- ASSETS Current assets: Cash and cash equivalents $ 2,579.4 $ 2,284.0 Short-term investments 378.1 561.9 Accounts receivable, net of allowances 597.9 578.3 Deferred tax assets, net 140.4 79.8 Prepaid expenses and other current assets 184.0 199.9 -------------- -------------- Total current assets 3,879.8 3,703.9 Property and equipment, net 905.7 882.3 Long-term investments 521.2 1,251.9 Restricted cash and investments 71.6 89.5 Purchased intangible assets, net 115.1 106.9 Goodwill 4,071.3 4,057.7 Other long-term assets 158.9 233.8 -------------- -------------- Total assets $ 9,723.6 $ 10,326.0 ============== ============== LIABILITIES AND STOCKHOLDERS' EQUITY Current liabilities: Accounts payable $ 222.2 $ 200.4 Accrued compensation 180.6 273.9 Deferred revenue 772.5 705.8 Other accrued liabilities 271.0 261.3 -------------- -------------- Total current liabilities 1,446.3 1,441.4 Long-term debt 1,348.9 999.3 Long-term deferred revenue 381.7 363.5 Long-term income taxes payable 121.7 114.4 Other long-term liabilities 115.5 105.2 -------------- -------------- Total liabilities 3,414.1 3,023.8 Total stockholders' equity 6,309.5 7,302.2 -------------- -------------- Total liabilities and stockholders' equity $ 9,723.6 $ 10,326.0 ============== ============== Juniper Networks, Inc. Preliminary Condensed Consolidated Statements of Cash Flows (in millions) (unaudited) Three Months Ended March 31, 2014 2013 -------------- -------------- Cash flows from operating activities: Net income $ 110.6 $ 91.0 Adjustments to reconcile net income to net cash provided by (used in) operating activities: Share-based compensation 60.8 49.9 Depreciation, amortization, and accretion 48.1 51.8 Restructuring and other charges 122.4 7.7 Deferred income taxes (44.5) 15.7 Gain on investments, net (166.2) (2.3) Excess tax benefits from share-based compensation (6.7) (1.1) Loss on disposal of fixed assets 0.8 0.1 Changes in operating assets and liabilities, net of effects from acquisitions: Accounts receivable, net (15.7) (94.3) Prepaid expenses and other assets 35.5 (53.6) Accounts payable 19.2 9.1 Accrued compensation (92.0) (75.2) Income taxes payable 21.2 (38.4) Other accrued liabilities (50.3) (26.5) Deferred revenue 82.8 57.2 -------------- -------------- Net cash provided by (used in) operating activities 126.0 (8.9) -------------- -------------- Cash flows from investing activities: Purchases of property and equipment (57.3) (71.5) Purchases of available-for-sale investments (327.1) (582.2) Proceeds from sales of available-for-sale investments 1,221.4 331.8 Proceeds from maturities of available-for- sale investments 79.3 54.0 Purchases of trading investments (1.8) (1.5) Proceeds from sales of privately-held investments 2.5 1.6 Purchases of privately-held investments (1.7) (7.3) Payments for business acquisitions, net of cash and cash equivalents acquired (27.1) (10.0) Changes in restricted cash 25.0 -- -------------- -------------- Net cash provided by (used in) investing activities 913.2 (285.1) -------------- -------------- Cash flows from financing activities: Proceeds from issuance of common stock 101.2 65.0 Purchases and retirement of common stock (905.8) (132.5) Purchase of equity forward contract (300.0) -- Issuance of long-term debt, net 346.5 -- Payment for capital lease obligation (0.4) (1.4) Customer financing arrangements 8.0 (2.3) Excess tax benefits from share-based compensation 6.7 1.1 -------------- -------------- Net cash used in financing activities (743.8) (70.1) -------------- -------------- Net increase (decrease) in cash and cash equivalents 295.4 (364.1) Cash and cash equivalents at beginning of period 2,284.0 2,407.8 -------------- -------------- Cash and cash equivalents at end of period $ 2,579.4 $ 2,043.7 ============== ============== Juniper Networks, Inc. Cash, Cash Equivalents, and Investments (in millions) (unaudited) March 31, December 31, 2014 2013 -------------- -------------- Cash and cash equivalents $ 2,579.4 $ 2,284.0 Short-term investments 378.1 561.9 Long-term investments 521.2 1,251.9 Total $ 3,478.7 $ 4,097.8 ============== ==============

Investor Relations Lisa Hartman Juniper Networks (408) 936-6123 lisah@juniper.net Media Relations Cindy Ta Juniper Networks (408) 936-6131 cta@juniper.net

SUNNYVALE, CA -- (Marketwired) -- 04/22/14 -- Juniper Networks (NYSE: JNPR)Q1 2014 Financial Highlights:Juniper Networks (NYSE: JNPR), the industry leader in network innovation, today reported preliminary financial results for the three months ended March 31, 2014 and provided its outlook for the three months ending June 30, 2014. Net revenues for the first quarter of 2014 increased 10% year-over-year and decreased 8% sequentially to $1,170 million. Juniper's operating margin for the first quarter of 2014 decreased to (0.5)% on a GAAP basis including $122 million of restructuring and other charges, from 15.3% in the fourth quarter of 2013, and decreased from 8.2% in the first quarter of 2013. Non-GAAP operating margin for the first quarter of 2014 decreased to 17.2% from 21.9% in the fourth quarter of 2013, and increased from 15.7% in the first quarter of 2013. Juniper posted GAAP net income of $110.6 million, or $0.22 per diluted share for the first quarter of 2014. The GAAP diluted income per share includes a $0.33 gain on the sale of minority equity investments offset by a $0.25 impact from restructuring and other charges. Non-GAAP net income was $142.6 million, or $0.29 per diluted share for the first quarter of 2014. Non-GAAP net income per diluted share decreased 33% compared to the fourth quarter of 2013, and increased 21% compared to the first quarter of 2013. The reconciliation between GAAP and non-GAAP results of operations is provided in a table immediately following the Preliminary Net Revenue by Market table below. "Juniper delivered solid first quarter results with strong year-over-year revenue growth. We are seeing continued demand from our customers reflecting a significant opportunity to capture share in meaningful, high-growth Cloud-Builder and High IQ networking across both service provider and enterprise markets," said Shaygan Kheradpir, chief executive officer of Juniper Networks. "I am very pleased with the disciplined approach we have taken with our Integrated Operating Plan. We have sharpened our focus on Cloud-Builders and High IQ networks with the ensemble of our products in routing, switching, security, network management, control and analytics; we have implemented an optimized One-Juniper structure; and we introduced a robust capital allocation program. While there is still work to do, I am confident that we have the right strategy in place to drive profitable growth and deliver significant value to shareholders." "I am pleased with our first quarter results, which reflect our seventh consecutive quarter of year-over-year revenue growth and our fifth consecutive quarter of earnings growth," said Robyn Denholm, chief financial and operations officer of Juniper Networks. "During the quarter we generated strong operating cash flows, drove operating margin expansion -- ahead of our Integrated Operating Plan cost reduction activities -- and initiated a $1.2 billion accelerated share repurchase program. Our revenues continue to diversify and we are well-positioned for continued growth, driven by the solid underlying performance across our business." Other Financial HighlightsTotal cash, cash equivalents, and investments as of March 31, 2014 were $3,479 million, compared to $4,098 million as of December 31, 2013, and $3,672 million as of March 31, 2013. Juniper's net cash flow from operations for the first quarter of 2014 was $126 million, compared to $390 million in the fourth quarter of 2013, and net cash outflow of ($9) million in the first quarter of 2013. Days sales outstanding in accounts receivable or "DSO" was 46 days in the first quarter of 2014, compared to 41 days in the prior quarter, and 45 days in the first quarter of 2013. During the first quarter of 2014, Juniper Networks initiated a $1.2 billion accelerated share repurchase program, of which $900 million of shares were initially delivered. Capital expenditures were $57.3 million and depreciation and amortization of intangible assets expense was $46.1 million during the first quarter of 2014. OutlookJuniper's outlook for the second quarter ending June 30, 2014 reflects its expectation that overall demand will remain healthy. The Company is focused on continued innovation and executing on its Integrated Operating Plan. Juniper Networks estimates:All forward-looking non-GAAP measures exclude estimates for amortization of intangible assets, share-based compensation expense, acquisition-related charges, restructuring and related costs, impairment charges, litigation settlements and resolutions, non-routine stockholder activities, gain or loss on equity investments, non-recurring income tax adjustments, valuation allowance on deferred tax assets and income tax effect of non-GAAP exclusions. A reconciliation of non-GAAP guidance measures to corresponding GAAP measures is not available on a forward-looking basis. Change in Reporting StructureIn the first quarter of 2014, Juniper announced an Integrated Operating Plan or "IOP" to refocus the Company's strategy, optimize its structure, and improve operational efficiencies. In connection with the IOP, Juniper realigned its R&D organizations previously reported under Platform Systems Division or "PSD" and Software Solutions Division or "SSD", into an optimized One-Juniper structure now called Juniper Development and Innovation or "JDI." As a result, Juniper is no longer reporting PSD or SSD as reportable segments. Juniper will continue to provide revenue details by product, geographic region and by market, and the historical amounts for these categorizations have not changed. Conference Call WebcastJuniper Networks will host a conference call webcast today, April 22, 2014, at 2:00 pm (Pacific Daylight Time), to be broadcast live over the Internet at http://investor.juniper.net/investor-relations/default.aspx . To participate via telephone in the US, the toll free dial-in number is 1-877-407-8033. Outside the US, dial +1-201-689-8033. Please call 10 minutes prior to the scheduled conference call time. The webcast replay will be archived on the Juniper Networks website. About Juniper NetworksJuniper Networks (NYSE: JNPR) delivers innovation across routing, switching and security. From the network core down to consumer devices, Juniper Networks' innovations in software, silicon and systems transform the experience and economics of networking. Additional information can be found at Juniper Networks ( www.juniper.net ) or connect with Juniper on Twitter and Facebook . Juniper Networks and Junos, are registered trademarks of Juniper Networks, Inc. in the United States and other countries. The Juniper Networks Logo, the Junos logo, and QFabric are trademarks of Juniper Networks, Inc. All other trademarks, service marks, registered trademarks, or registered service marks are the property of their respective owners. Safe HarborStatements in this release concerning Juniper Networks' business outlook, economic and market outlook, future financial and operating results, and overall future prospects are forward-looking statements that involve a number of uncertainties and risks. Actual results or events could differ materially from those anticipated in those forward-looking statements as a result of certain factors, including: general economic and political conditions globally or regionally; business and economic conditions in the networking industry; changes in overall technology spending and spending by communication service providers and major customers; the network capacity requirements of communication service providers; contractual terms that may result in the deferral of revenue; increases in and the effect of competition; the timing of orders and their fulfillment; manufacturing and supply chain constraints; ability to establish and maintain relationships with distributors, resellers and other partners; variations in the expected mix of products sold; changes in customer mix; changes in geography mix; customer and industry analyst perceptions of Juniper Networks and its technology, products and future prospects; delays in scheduled product availability; market acceptance of Juniper Networks products and services; rapid technological and market change; adoption of regulations or standards affecting Juniper Networks products, services or the networking industry; the ability to successfully acquire, integrate and manage businesses and technologies; product defects, returns or vulnerabilities; the ability to recruit and retain key personnel; significant effects of tax legislation and judicial or administrative interpretation of tax regulations; currency fluctuations; litigation settlements and resolutions; the potential impact of activities related to the execution of the Juniper Networks Integrated Operating Plan; and other factors listed in Juniper Networks' most recent report on Form 10-K filed with the Securities and Exchange Commission. All statements made in this press release are made only as of the date set forth at the beginning of this release. Juniper Networks undertakes no obligation to update the information in this release in the event facts or circumstances subsequently change after the date of this press release. Juniper Networks believes that the presentation of non-GAAP financial information provides important supplemental information to management and investors regarding financial and business trends relating to the company's financial condition and results of operations. For further information regarding why Juniper Networks believes that these non-GAAP measures provide useful information to investors, the specific manner in which management uses these measures, and some of the limitations associated with the use of these measures, please refer to the discussion below. The following tables and reconciliations can also be found on our Investor Relations website at http://investor.juniper.net/investor-relations/default.aspx Discussion of Non-GAAP Financial Measures This press release, including the tables above and below, includes the following non-GAAP financial measures derived from our Preliminary Condensed Consolidated Statements of Operations: product gross margin, product gross margin as a percentage of product revenue; service gross margin; service gross margin as a percentage of service revenue; gross margin; gross margin as a percentage of revenue; research and development expense; sales and marketing expense; general and administrative expense; operating expense; operating income; operating margin; provision for income taxes; income tax rate; net income; and net income per share. These measures are not presented in accordance with, nor are they a substitute for U.S. generally accepted accounting principles or GAAP. In addition, these measures may be different from non-GAAP measures used by other companies, limiting their usefulness for comparison purposes. The non-GAAP financial measures used in the table above should not be considered in isolation from measures of financial performance prepared in accordance with GAAP. Investors are cautioned that there are material limitations associated with the use of non-GAAP financial measures as an analytical tool. In particular, many of the adjustments to our GAAP financial measures reflect the exclusion of items that are recurring and will be reflected in our financial results for the foreseeable future. We utilize a number of different financial measures, both GAAP and non-GAAP, in analyzing and assessing the overall performance of our business, in making operating decisions, forecasting and planning for future periods, and determining payments under compensation programs. We consider the use of the non-GAAP measures presented above to be helpful in assessing the performance of the continuing operation of our business. By continuing operations we mean the ongoing revenue and expenses of the business excluding certain items that render comparisons with prior periods or analysis of on-going operating trends more difficult, such as expenses not directly related to the actual cash costs of development, sale, delivery or support of our products and services, or expenses that are reflected in periods unrelated to when the actual amounts were incurred or paid. Consistent with this approach, we believe that disclosing non-GAAP financial measures to the readers of our financial statements provides such readers with useful supplemental data that, while not a substitute for financial measures prepared in accordance with GAAP, allows for greater transparency in the review of our financial and operational performance. In addition, we have historically reported non-GAAP results to the investment community and believe that continuing to provide non-GAAP measures provides investors with a tool for comparing results over time. In assessing the overall health of our business for the periods covered by the table above and, in particular, in evaluating the financial line items presented in the table above, we have excluded items in the following three general categories, each of which are described below: Acquisition-Related Charges, Other Items, and Share-Based Compensation Related Items. We also provide additional detail below regarding the shares used to calculate our non-GAAP net income per share. Notes identified for line items in the table above correspond to the appropriate note description below. Additionally, with respect to future financial guidance provided on a non-GAAP basis, we have excluded estimates for amortization of intangible assets, share based compensation expenses, acquisition related charges, restructuring charges, litigation settlement and resolution charges, gain or loss on equity investments, non-recurring income tax adjustments, valuation allowance on deferred tax assets, and income tax effect of non-GAAP exclusions. Note A: Acquisition-Related Charges. We exclude certain expense items resulting from acquisitions including the following, when applicable: (i) amortization of purchased intangible assets associated with our acquisitions; (ii) compensation related to acquisitions; and (iii) acquisition-related charges. The amortization of purchased intangible assets associated with our acquisitions results in our recording expenses in our GAAP financial statements that were already expensed by the acquired company before the acquisition and for which we have not expended cash. Moreover, had we internally developed the products acquired, the amortization of intangible assets, and the expenses of uncompleted research and development would have been expensed in prior periods. Accordingly, we analyze the performance of our operations in each period without regard to such expenses. In addition, acquisitions result in non-continuing operating expenses, which would not otherwise have been incurred by us in the normal course of our business operations. For example, we have incurred deferred compensation charges related to assumed options and transition and integration costs such as retention bonuses and acquisition-related milestone payments to acquired employees. We believe that providing non-GAAP information for acquisition-related expense items in addition to the corresponding GAAP information allows the users of our financial statements to better review and understand the historic and current results of our continuing operations, and also facilitates comparisons to less acquisitive peer companies. Note B: Other Items. We exclude certain other items that are the result of either unique or unplanned events including the following, when applicable: (i) restructuring and related costs; (ii) impairment charges; (iii) gain or loss on legal settlement, net of related transaction costs; (iv) retroactive impacts of certain tax settlements; (v) significant effects of tax legislation and judicial or administrative interpretation of tax regulations; (vi) gain or loss on equity investments; (vii) the income tax effect on our financial statements of excluding items related to our non-GAAP financial measures; and (viii) non-routine stockholder activities. It is difficult to estimate the amount or timing of these items in advance. Restructuring and impairment charges result from events, which arise from unforeseen circumstances, which often occur outside of the ordinary course of continuing operations. Although these events are reflected in our GAAP financials, these unique transactions may limit the comparability of our on-going operations with prior and future periods. In the case of legal settlements, these gains or losses are recorded in the period in which the matter is concluded or resolved even though the subject matter of the underlying dispute may relate to multiple or different periods. As such, we believe that these expenses do not accurately reflect the underlying performance of our continuing operations for the period in which they are incurred. Similarly, the retroactive impacts of certain tax settlements and significant effects of retroactive tax legislation are unique events that occur in periods that are generally unrelated to the level of business activity to which such settlement or legislation applies. We believe this limits comparability with prior periods and that these expenses do not accurately reflect the underlying performance of our continuing business operations for the period in which they are incurred. Whether we realize gains or losses on equity investments is based primarily on the performance and market value of those independent companies. Accordingly, we believe that these gains and losses do not reflect the underlying performance of our continuing operations. We also believe providing financial information with and without the income tax effect of excluding items related to our non-GAAP financial measures provide our management and users of the financial statements with better clarity regarding the on-going performance and future liquidity of our business. Because of these factors, we assess our operating performance both with these amounts included and excluded, and by providing this information, we believe the users of our financial statements are better able to understand the financial results of what we consider our continuing operations. Note C: Share-Based Compensation Related Items. We provide non-GAAP information relative to our expense for share-based compensation and related payroll tax. We began to include share-based compensation expense in our GAAP financial measures in accordance with Financial Accounting Standards Board ("FASB") Accounting Standards Codification ("ASC") Topic 718, Compensation - Stock Compensation ("FASB ASC Topic 718"), in January 2006. Because of varying available valuation methodologies, subjective assumptions and the variety of award types, which affect the calculations of share-based compensation, we believe that the exclusion of share-based compensation allows for more accurate comparisons of our operating results to our peer companies. Further, we believe that excluding share-based compensation expense allows for a more accurate comparison of our financial results to previous periods during which our equity-based awards were not required to be reflected in our income statement. Share-based compensation is very different from other forms of compensation. A cash salary or bonus has a fixed and unvarying cash cost. For example, the expense associated with a $10,000 bonus is equal to exactly $10,000 in cash regardless of when it is awarded and who it is awarded by. In contrast, the expense associated with an award of an option for 1,000 shares of share is unrelated to the amount of compensation ultimately received by the employee; and the cost to the company is based on a share-based compensation valuation methodology and underlying assumptions that may vary over time and that does not reflect any cash expenditure by the company because no cash is expended. Furthermore, the expense associated with granting an employee an option is spread over multiple years unlike other compensation expenses which are more proximate to the time of award or payment. For example, we may be recognizing expense in a year where the stock option is significantly underwater and is not going to be exercised or generate any compensation for the employee. The expense associated with an award of an option for 1,000 shares of stock by us in one quarter may have a very different expense than an award of an identical number of shares in a different quarter. Finally, the expense recognized by us for such an option may be very different than the expense to other companies for awarding a comparable option, which makes it difficult to assess our operating performance relative to our competitors. Similar to share-based compensation, payroll tax on stock option exercises is dependent on our stock price and the timing and exercise by employees of our share-based compensation, over which our management has little control, and as such does not correlate to the operation of our business. Because of these unique characteristics of share-based compensation and the related payroll tax, management excludes these expenses when analyzing the organization's business performance. We also believe that presentation of such non-GAAP information is important to enable readers of our financial statements to compare current period results with periods prior to the adoption of FASB ASC Topic 718. Note D: Non-GAAP Net Income Per Share Items. We provide diluted non-GAAP net income per share. The diluted non-GAAP income per share includes additional dilution from potential issuance of common stock, except when such issuances would be anti-dilutive.Source: Juniper Networks"																					1	0	1
149558	Juniper Cost Cuts in Focus, F5's Product Turnaround Offers Hope, Say  ...	http://blogs.barrons.com/techtraderdaily/2014/04/22/juniper-cost-cuts-in-focus-f5s-product-turnaround-offers-hope-say-needham-isi/	Barron's \(blog\)	b	d_CswVIPiQ_gM5M9wJF8Gi1oa57aM	blogs.barrons.com	2014-04-23 04:29:34	1		en	focus,eps,view,rating,security,cost,f5s,offers,turnaround,juniper,f5,product,needham,hope,isi,shares,strong,sales,say	"Text size

This week brings a slew of reports among networking vendors, including Juniper Networks (JNPR), tonight, F5 Networks (FFIV) and Infinera (INFN) tomorrow, and Alliance Fiber Optic (AFOP) and Silicom (SILC) on Thursday, and Street networking analysts have been highlighting things to look for.

Alex Henderson with Needham & Co. thinks Juniper could miss top line expectations of $1.15 billion, and may beat on the bottom line 29-cent EPS consensus estimate, given the company's making deep cuts to expenses after the restructuring plan announced in February:

The story at Juniper is almost certainly going to be the restructuring. Our forecast for Juniper on an EPS basis is probably too low. They are cutting costs at a more rapid pace than expected or initially indicated. On the other hand, we are concerned that they are likely under cutting the company's ability to grow and retrenching deeply on the enterprise portion of their business. They may beat our forecast and that more of a sell signal than a Buy signal – we remain firmly on the sidelines despite the good cost news. We are worried that they will be unable to grow after the current crop of new products has its short period of revenue support […] We are nervous about the top line and think the cost cuts are deeper and faster than expected helping provide upside to EPS. We would not be surprised to see lower Revenues and higher EPS for the year.

He expects F5 to beat the average estimate for $414 million and $1.25, helped by several things, including the build-out of 10-gigabit per second connections in data centers:

F5 has several things going for it in the quarter: 1) easy compares. 2) Strong orders in late CY4Q/FY1Q sloshed into January deliveries, 3) we think there was a strong March order environment. Combined with new product strength, stronger security sales and the recent new chassis launch, F5 should be in good shape for the quarter. If they post a strong CY1Q they should be set up well through the September quarter. We also think F5 plays well against our thesis of a stronger demand environment due to the rising adoption of 10G server to switch connections. This drives higher speed and larger boxes and helps F5 ASPs. We are inclined to be more constructive on F5, Radware, and Silicom based on this outlook.

Henderson has a Hold rating on Juniper shares, and a Buy rating on F5, with a $119 price target.

On the other hand, Brian Marshall of ISI Group today reiterates a Strong Buy rating on shares of Juniper and a $30 price target, offering some favorable views on the cost cutting.

He has the same $1.15 billion and 29 cents per share as the Street, and thinks cost cutting will be a catalyst for the shares, especially if there's further cost-cutting to come:

In our view, JNPR took many of the tough decisions this year that had been put off for too long in the name of investing for growth. Following the announcement of a ~6% reduction in force or RIF, we have much greater visibility to JNPR's stated target of ~$160mil in annualized cost savings in 1Q15 (vs. 4Q13 base of ~$539mil). Our rough math suggests the RIF alone could account for ~$100mil of the savings (assuming ~$165k all-in costs per employee). While a difficult action, we believe it's a sign new management under CEO Kheradpir is more realistic about its ambitions and target markets rather than pursuing growth in non-strategic areas. Following the dissolution of its ADC (application delivery controller) joint partnership with RVBD, we wouldn't be surprised if JNPR also took a close look winding down its enterprise WiFi business (i.e., Trapeze acquisition) or pursuing a narrower focus in security / switching products (e.g., emphasis on datacenter and service provider segments vs. campus/branch).

As for F5, it can look forward to a bounce-back in sales as a result of the company's revamp of its products last year, writes Marshall:

While the stock up ~15% year-to-date (and up ~30% from Nov-13), we believe there is more upside potential over the course of CY14. In our view, upgraded hardware appliance offerings have made it easier to sell new software modules (i.e., security) as price/performance becomes more compelling. High-margin security module sales could offer potential for ~15% EPS accretion (or ~$0.80 EPS) on top of our ~$5.37 CY14 estimate over an ~18 month period as FFIV gradually addresses a greater portion of the ~$10bil network security market. We wouldn't be surprised to get visibility on CY15 earnings power approaching ~$7.00 with continued core business growth as well as contribution from other initiatives (e.g., security, LTE/Traffix deployments, CSCO ACE replacement deals) which can have longer sales cycles. If our security sensitivity plays out, we see upside potential to ~$140 on the stock based on an unchanged ~20x multiple and ~$7.00 of earnings power.

Marshall has a Buy rating on F5, and a $125 price target.

Marshall's positive view reflects his view that enterprise budgets are becoming more relaxed, less constrictive, but offset by the fact that newer technologies are causing some customers to pause in spending:

As a group, we expect enterprise infrastructure earnings reports to be largely in-line with gradual strengthening through the year as pent- up demand from two years of higher storage/networking capacity utilizations is satisfied. While we expect IT budgets to improve, large industry transitions (e.g., software-defined networking [SDN], software-defined storage [SDS], hybrid clouds, etc.) as well as new/immature technology offerings are making some organizations a little bit more hesitant before committing to new IT architectures.

Juniper shares today are up 47 cents, or 1.8%, at $25.89, while F5 shares are up $1, or 0.9%, at $109.77."																					1	0	1
149563	SC Magazine subscribers honour Juniper Networks in 2014 SC Awards  ...	http://www.itweb.co.za/office/securedata/PressRelease.php\?StoryID=248330	ITWeb	b	d_CswVIPiQ_gM5M9wJF8Gi1oa57aM	www.itweb.co.za	2014-04-23 04:29:35	1			networks,management,security,ngfw,edge,juniper,enterprise,today,organisations,network	"Juniper Networks (NYSE: JNPR), the industry leader in network innovation, today announced powerful new capabilities in its Next-Generation Firewall (NGFW) solutions for protecting the enterprise edge, offering added security, control and efficiency while being easier to deploy and manage.

As security threats to enterprises continue to get more advanced and targeted, organisations need firewalls to provide added layers of security without adding complexity. Yet, the bulk of organizations are only now beginning to consider what NGFW can do for them. According to Gartner, less than 20% of enterprise Internet connections today are secured using NGFWs, and that by year-end 2014, this will rise to 35% of the installed base, with 70% of new enterprise edge purchases being NGFWs.(1)

The capabilities introduced today as part of Juniper Networks NGFW enable large organisations to manage a broad range of deployments and use cases while simplifying administrative overhead. Juniper's solution also offers simplified and centralised management and an open services platform for essential security features including intrusion prevention system (IPS), unified threat management (UTM) and application visibility. Further, the technology helps optimise enterprise resources for business-critical activities by prioritising who gets access to what applications and what applications get prioritised on the network."																					1	0	1
170956	Target takes security steps with new executive, MasterCard deal	http://www.charlotteobserver.com/2014/04/29/4874760/target-takes-security-steps-with.html	Charlotte Observer	b	d_hYxaw1xsoBwDMUlRM0FnlrHDrkM	www.charlotteobserver.com	2014-04-30 10:09:11	1		en	prosecutors,executive,steps,forfeit,takes,mastercard,empire,service,dropped,observer,racist,volunteer,deal,target,security,smollett,charlotte,jussie,faking	Prosecutors dropped all charges against Jussie Smollett after the "Empire" actor accused of faking a racist, anti-gay attack on himself agreed to do volunteer service and forfeit his $10,000 in bail.																					1	0	1
170966	Target hires IT chief, switches to chip-and-PIN cards	http://journalstar.com/business/local/target-hires-it-chief-switches-to-chip-and-pin-cards/article_f9904df2-35ec-536c-9e05-d55ac42c70b9.html	Lincoln Journal Star	b	d_hYxaw1xsoBwDMUlRM0FnlrHDrkM	journalstar.com	2014-04-30 10:09:13	1		en	subscription,surveysthanks,upgrade,super,sale,chief,unlimited,target,switches,subscribersorry,skip,week,plus,chipandpin,hires,cards	"SUPER SALE: $3 for 3 months of Digital Plus Then $2.49 a week. Cancel anytime. ✓ E-Edition PDF of newspaper ✓ HuskerExtra Sports Exclusive included ✓ Unlimited access on any device ✓ Skip article surveys

Thanks for being a subscriber.

Sorry, your subscription does not include this content.

Please call 877-760-6006 to upgrade your subscription."																					1	0	1
183223	Dancing With The Stars' Guest Judge And Dance Moms Star Abby Lee Miller  ...	http://www.entertainmentwise.com/news/148392/Dancing-With-The-Stars-Guest-Judge-And-Dance-Moms-Star-Abby-Lee-Miller-Clashes-With-Professional-Dancers	Entertainmentwise	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	www.entertainmentwise.com	2014-05-06 15:59:49	1		en	straight,experience,cookies,young,best,site,ensure,abby,gay,assume,lee,ethnicity,photos,website,continue,miller,happy,wiki	We use cookies to ensure that we give you the best experience on our website. If you continue to use this site we will assume that you are happy with it.																					1	0	0
183227	'Dancing with the Stars' vs 'Dance Moms': Maks meets Abby Lee Miller	http://siouxcityjournal.com/blogs/bruceblog/dancing-with-the-stars-vs-dance-moms-maks-meets-abby/article_e4be3d4a-d4c5-11e3-ae0c-001a4bcf887a.html	Sioux City Journal \(blog\)	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	siouxcityjournal.com	2014-05-06 15:59:50	1		en	moms,sent,dance,saving,miller,savedthere,posts,lee,maks,email,youll,stars,bruce,vs,meets,notifications,abby,dancing,problem	"Close Get email notifications on Bruce Miller daily!

Your notification has been saved.

There was a problem saving your notification.

Whenever Bruce Miller posts new content, you'll get an email delivered to your inbox with a link.

Email notifications are only sent once a day, and only if there are new matching items."																					1	0	1
183231	Dancing With the Stars Results: Who Got All 10s? Who Got the Heave-Ho?	http://www.thehollywoodgossip.com/2014/05/dancing-with-the-stars-results-who-got-the-heave-ho/	The Hollywood Gossip	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	www.thehollywoodgossip.com	2014-05-06 15:59:51	1		en	10s,stars,purdy,dancing,amy,36,results,dance,white,heaveho,watch,38	"Monday's Dancing with the Stars Season 18 Episode 8 showcased some typically talented performances. Even the week's guest judge was impressed ...

... Abby Lee Miller!

If you watch Dance Moms online, you know she's a tough cookie (and that's as nicely as we can put it). So to win 9s and 10s from her is no small feat.

Who did just that?

Let's take a look at the performances and scores on Dancing with the Stars Season 18 Episode 8, and see who lived to dance another week on ABC ...

Amy Purdy and Charlie White took the lead away from Meryl Davis, who actually scored at the bottom of the pack last night with Maksim Chmerkovskiy.

Both scored all 10s last night. Impressive work, especially considering that Amy Purdy was hospitalized just a week ago after her performance on the show.

Each dancer performed an individual routine, followed by a dance duel against another star. The full scoreboard from last night's Dancing with the Stars:

Amy Purdy and Derek Hough: 10, 10, 10, 10 = 40 + 39 = 79

Charlie White and Sharna Burgess: 10, 10, 10, 10 = 40 + 38 = 78

James Maslow and Peta Murgatroyd: 8, 9, 10, 9 = 36 + 39 = 75

Candace Cameron Bure and Mark Ballas: 9, 9, 9, 9 = 36 + 38 = 74

Danica McKellar and Val Chmerkovskiy: 10, 9, 9, 10 = 38 + 34 = 72

Meryl Davis and Maksim Chmerkovskiy: 9, 9, 8, 10 = 36 + 34 = 70

In jeopardy: Danica, James and Candace. Who went home?

Danica.

While we're sad to see the beautiful former child star go, especially after two 10s, someone had to, and this year's field is particularly evenly matched.

"It's been absolutely amazing. I've had the best time ever," she said with a smile. "And I didn't want to see any of them eliminated so I guess it worked out."

What a sweetheart. It's like she's the anti-Abby Lee Miller. Can you imagine her reacting that way to having her winning streak snapped on Dance Moms?

We cannot. See below ...

Speaking of fights, it will be a battle royale in next week's semifinals. Who will advance when Meryl, Amy, Candace, James and Charlie duke it out?

It will be a treat to watch, that's for sure. Follow the link to watch Dancing with the Stars online at TV Fanatic and share your comments below ..."																					1	0	0
183237	'Dancing With the Stars' recap: Dueling celebs, and one sad farewell	http://www.latimes.com/entertainment/tv/showtracker/la-et-st-dancing-with-the-stars-recap-20140505-story.html	Los Angeles Times	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	www.latimes.com	2014-05-06 15:59:52	1		en	quickstep,dueling,bit,stars,struggled,recap,farewell,dancing,celebs,looked,weeks,trademark,olympian,charlie,white,thoroughbred,sad	Charlie White has struggled a bit in the last couple of weeks. The Olympian admitted that he was focusing on the scores a little too much, and losing a bit of his trademark positivity. But goldilocks and Sharna Burgess were able to find a routine that was just right in their quickstep (and the pro looked great in a low-plunging dress that looked as though it came from the Amy Adams "American Hustle" collection). The quickstep had more hearts scrawled on it than a schoolgirl crush, so it's only natural that the judges would also feel the love. Though the comments didn't exactly set it up for a perfect 40 score. Len was coy on his paddle position, and Carrie Ann said the Olympian finally broke his stride and "gone a step beyond." But Abby was all about Charlie slicking back his hair and straightening his knee up the stairs. And while Bruno likened Charlie to a thoroughbred at the Kentucky Derby off the starting block, he also said "you were not quite clean on the stops."																					1	0	1
183267	'DWTS' Recap: Abby Lee Miller's Attitude Makes Unfair Elimination Even Worse	http://thestir.cafemom.com/entertainment/172051/dwts_recap_abby_lee_millers	The Stir	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	thestir.cafemom.com	2014-05-06 16:00:01	1		en	dwts,annoying,recap,um,abby,millers,hell,lee,unfair,makes,elimination,miller,totally,worse,val,tonight,attitude,ugh	"Ugh. For the love of Pete, can we please cool it with the guest judges this season, ABC? Um, was Abby Lee Miller annoying as hell on Dancing With the Stars tonight, or was Abby Lee Miller ANNOYING AS HELL on DWTS tonight?

I know she was there to critique the performances, but she totally took things too far -- especially when she made fun of Meryl Davis' feet, for crying out loud! Thankfully Maksim and Val Chmerkovskiy both seemed to be fairly effective at shutting her up -- but we still had to endure two hours of her being a major buzz kill.

I mean, some of the dances tonight were nothing short of extraordinary, and then she had to go and put a negative spin on everything, which really sucked.

Advertisement"																					1	0	1
183272	'Dancing With the Stars' TV Recap: Who Danced It Best?	http://blogs.wsj.com/speakeasy/2014/05/05/dancing-with-the-stars-tv-recap-who-danced-it-best-2/	Wall Street Journal \(blog\)	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	blogs.wsj.com	2014-05-06 16:00:03	1		en	tanner,week,tom,stars,best,winnie,tv,recap,upper,dancing,didnt,danica,trying,talk,val,danced	"In the battle of 1990s ABC sitcom stars, D.J. Tanner defeated Winnie Cooper, as Danica McKellar (and partner Val Chmerkovskiy) were eliminated this week on “Dancing with the Stars.”

Danica, normally on the upper end of the leaderboard, suffered numerically and physically last week as a result of a fractured rib. Danica, a fan of the show, said she didn’t want to see anyone else go home, so that left … well, her. As she departed, host Tom Bergeron said he’d been trying to talk Danica into doing the show for two years. She assured Tom she didn’t have regrets, and she received a lot of hugs from her fellow celebrities."																					1	0	1
183278	Dancing with the Stars Results Surprise!	http://www.gossipcop.com/danica-mckellar-eliminated-dancing-with-the-stars-voted-off-val-chmerkovskiy-dwts-results-may-5-2014/	GossipCop	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	www.gossipcop.com	2014-05-06 16:00:05	1		en	dwts,banning,getting,britney,stars,married,dancing,truth,spears,dad	Truth About Britney Spears’ Dad Banning Her From Getting Married																					1	0	1
183293	Dancing with the Stars 2014 Results Tonight May 5: Who Gets Eliminated?	http://news.lalate.com/2014/05/05/dancing-with-the-stars-2014-results-tonight-may-5-who-gets-eliminated/	LALATE	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	news.lalate.com	2014-05-06 16:00:09	1		en	week,stars,gets,candace,dancing,scores,eliminated,elimination,including,danica,results,lalate,tonight,numbers	"

ST LOUIS (LALATE) – Who will get eliminated in Dancing with the Stars result tonight for 5/5/14, who will get sent home in DWTS this evening, and will there be a surprise announcement? Dancing with the Stars 2014 results tonight for May 5, 2014 are prompting elimination predictions, targeting Danica McKellar and Val Chmerkovskiy. Last week, many fans thought Candace Cameron Bure would be get the DWTS elimination announcement. But NeNe Leakes was sent home.

Candace Cameron Bure seemed a likely elimination last week. But this week, Dancing with the Stars 2014 elimination predictions are not focusing on Candace. They are focusing on Danica. Danica McKellar and Val Chmerkovskiy struggled last week on the salsa. They picked up a thirty-three compromised of three “8” scores. Danica followed stronger numbers including James Maslow and Peta Murgatroyd, earning a thirty-five on the salsa in group one. Leading the scores into the telecast was Amy Purdy and Derek Hough, producing a thirty-six on the rumba.

In group two, all the scores were higher than Danica’s numbers. Charlie White and Sharna Burgess impressed the judges, earning a thirty-six on the paso doble. Then what happened with Candace Cameron Bure and Mark Ballas? On the Argentine Tango they rebounded, producing a thirty-five. Finally another night delivered another round of great numbers from Meryl Davis and Maksim Chmerkovskiy. They salsa produced thirty-nine. With those numbers, the likely celebrity to be eliminated. But could there be a surprise with someone else like Candace? For live results as they happen tonight click HERE.

LALATE ABOUT THIS AUTHOR || Editor in Chief: Maria Stabile | Maria in ten years has propelled LALATE to become a leading news authority in sports, entertainment, and national news, LALATE has been cited in countless international newspapers (including the Wall Street Journal, New York Times and LA Times), international television news broadcasts including ABC News, books including The Iraq War: Origins and Consequences, tv programs including MTV News, and magazines. For over a decade, LALATE has been a proud licensed member of the St Louis, MO Press Club. || TO CONTACT THIS AUTHOR | Email Address: mstabile@lalate.com | Telephone: 314-400-8010 | Follow on Twitter: Twitter.com/LALATE | Biography: http://news.lalate.com/author/maria-stabile/ | LALATE Staff & Physical Address: http://news.lalate.com/staff/



"																					1	0	1
183306	Mark Ballas To Debut Single 'Get My Name' on 'Dancing With The Stars'	http://www.singersroom.com/content/2014-05-05/Mark-Ballas-To-Debut-Single-Get-My-Name-on-Dancing-With-The-Stars/	Singersroom News	e	d_hkNefz8uam2tMyhuI0QgziXPDCM	www.singersroom.com	2014-05-06 16:00:13	1		en	single,debut,stars,release,feel,writer,dancing,choreographer,working,studio,mark,ballas,sound	"Dance pro Mark Ballas will debut his first single on "Dancing With The Stars" this week.

Set for debut and release tonight, May 5, the single is titled "Get My Name."

"While collaborating in the studio with Timbaland's protege, producer, Wizz Dumb and Missy Elliott mentored writer Jo'zzy, Ballas' Get My Name touts a soulful but fun, funky pop sound. Together, they describe the co-written record as simply, "infectious and fresh," Ballas' management reports. "The Get My Name video, also dropping on May 5th, is visually stunning, shot in the contemporary, with a throwback feel, directed by Emmy-award winning choreographer, Derek Hough. The mash-up reflects Ballas' true musical style while showcasing the immense scope of his classical guitar training and musicianship."

"Get My Name" is being made available on iTunes and via 189 digital retail outlets globally.

Signed to BMG Publishing, songwriter-musician and Emmy-nominated dancer and choreographer Ballas had this to say, "I'm so excited about where my music is today. I have been in the studio working on this album for two years now and I feel like my sound has evolved and niched into something I am really proud of. This single is my first full studio release – looking forward to everyone hearing it!""																					1	0	1
211295	WHO alcohol report shows work needed	http://www.just-drinks.com/news/who-alcohol-report-shows-work-needed_id113681.aspx	just-drinks.com \(subscription\)	m	d_fZttD4zTqbgVMwDzj_ZPS8W5B_M	www.just-drinks.com	2014-05-13 15:47:28	1	2014-05-13 12:57:00		needed,health,access,offer,vat,today,spiritseurope,wehring,unlimited,alcohol,shows,plus,organization,justdrinks,youriskfree,work,youolly,report,world,global	"A Message From The Editor

Only paid just-drinks members have unlimited access to all our content - including 21 years of archives.

I am so confident you will love just-drinks membership that today I can offer you 30 days access for €1*.

It’s a fantastic offer – just for you.

Olly Wehring, editor of just-drinks

Olly's offer to you

Risk-free, money-back guarantee

* plus VAT if applicable"	A Message From The Editor Only paid just-drinks members unlimited access content - including 21 years archives I confident love just-drinks membership today I offer 30 days access €1* It’s fantastic offer – Olly Wehring, editor just-drinks Olly's offer Risk-free, money-back guarantee * plus VAT applicable	0	Olly Wehring,fantastic offer,day access,drink membership,unlimited access,drink,archive,confident,year,today,content,offer,Olly,editor,Editor,money,free,guarantee,risk,VAT,applicable,message	27	Olly,Olly,VAT	18	Olly Wehring,fantastic offer,day access,drink membership,unlimited access,drink,archive,confident,year,today,content,offer,Olly,editor,Editor,money,free,guarantee,risk,VAT,applicable,message	45	a messag from the editor onli paid just-drink member have unlimit access to all our content - includ 21 year of archiv i am so confid you will love just-drink membership that today i can offer you 30 day access for €1* it a fantast offer – just for you olli wehring, editor of just-drink olli offer to you risk-free, money-back guarante * plus vat if applic	1	a messag from the editor onli paid just-drink member unlimit access content - includ 21 year archiv i confid love just-drink membership today i offer 30 day access €1* it fantast offer – olli wehring, editor just-drink olli offer risk-free, money-back guarante * plus vat applic	1	messag editor paid just drink member unlimit access content includ archiv confid love just drink membership offer access fantast offer olli wehring editor just drink olli offer risk free money back guarante plus vat applic	1	"a message From the Editor 

 only pay just - drink member have unlimited access to all our content - include 21 year of archive.i be so confident you will love just - drink membership that today i can offer you 30 day access for € 1 *.it ’ a fantastic offer – just for you.olly Wehring , editor of just - drink 

 olly 's offer to you 

 Risk - free , money - back guarantee 

 * plus VAT if applicable"	148	"a message From the Editor 

 only pay just - drink member have unlimited access to all our content - include 21 year of archive.i am so confident you will love just - drink membership that today i can offer you 30 day access for € 1 *.it ’ a fantastic offer – just for you.olly Wehring , editor of just - drink 

 olly 's offer to you 

 Risk - free , money - back guarantee 

 * plus VAT if applicable"	147	message from the editor only pay just drink member have unlimited access our content include archive confident you will love just drink membership that can offer you access for fantastic offer just for you olly wehring editor just drink olly offer you risk free money back guarantee plus vat applicable	147	1	1	0
211296	GLOBAL: World Health Organization alcohol report shows work needed  ...	http://www.just-drinks.com/news/world-health-organization-alcohol-report-shows-work-needed-spiritseurope_id113681.aspx	just-drinks.com \(subscription\)	m	d_fZttD4zTqbgVMwDzj_ZPS8W5B_M	www.just-drinks.com	2014-05-13 15:47:28	1	2014-05-13 12:57:00		needed,health,access,offer,vat,today,spiritseurope,wehring,unlimited,alcohol,shows,plus,organization,justdrinks,youriskfree,work,youolly,report,world,global	"A Message From The Editor

Only paid just-drinks members have unlimited access to all our content - including 21 years of archives.

I am so confident you will love just-drinks membership that today I can offer you 30 days access for €1*.

It’s a fantastic offer – just for you.

Olly Wehring, editor of just-drinks

Olly's offer to you

Risk-free, money-back guarantee

* plus VAT if applicable"	A Message From The Editor Only paid just-drinks members unlimited access content - including 21 years archives I confident love just-drinks membership today I offer 30 days access €1* It’s fantastic offer – Olly Wehring, editor just-drinks Olly's offer Risk-free, money-back guarantee * plus VAT applicable	1	Olly Wehring,fantastic offer,day access,drink membership,unlimited access,drink,archive,confident,year,today,content,offer,Olly,editor,Editor,money,free,guarantee,risk,VAT,applicable,message	29	Olly,Olly,VAT	19	Olly Wehring,fantastic offer,day access,drink membership,unlimited access,drink,archive,confident,year,today,content,offer,Olly,editor,Editor,money,free,guarantee,risk,VAT,applicable,message	48	a messag from the editor onli paid just-drink member have unlimit access to all our content - includ 21 year of archiv i am so confid you will love just-drink membership that today i can offer you 30 day access for €1* it a fantast offer – just for you olli wehring, editor of just-drink olli offer to you risk-free, money-back guarante * plus vat if applic	1	a messag from the editor onli paid just-drink member unlimit access content - includ 21 year archiv i confid love just-drink membership today i offer 30 day access €1* it fantast offer – olli wehring, editor just-drink olli offer risk-free, money-back guarante * plus vat applic	1	messag editor paid just drink member unlimit access content includ archiv confid love just drink membership offer access fantast offer olli wehring editor just drink olli offer risk free money back guarante plus vat applic	1	"a message From the Editor 

 only pay just - drink member have unlimited access to all our content - include 21 year of archive.i be so confident you will love just - drink membership that today i can offer you 30 day access for € 1 *.it ’ a fantastic offer – just for you.olly Wehring , editor of just - drink 

 olly 's offer to you 

 Risk - free , money - back guarantee 

 * plus VAT if applicable"	156	"a message From the Editor 

 only pay just - drink member have unlimited access to all our content - include 21 year of archive.i am so confident you will love just - drink membership that today i can offer you 30 day access for € 1 *.it ’ a fantastic offer – just for you.olly Wehring , editor of just - drink 

 olly 's offer to you 

 Risk - free , money - back guarantee 

 * plus VAT if applicable"	154	message from the editor only pay just drink member have unlimited access our content include archive confident you will love just drink membership that can offer you access for fantastic offer just for you olly wehring editor just drink olly offer you risk free money back guarantee plus vat applicable	153	1	1	0
211328	Hastings man jailed for attempted murder of Wetherspoons' doorman	http://www.theargus.co.uk/NEWS/11207630.Man_jailed_for_attempted_murder_of_Wetherspoonss_doorman/	The Argus	m	d_fZttD4zTqbgVMwDzj_ZPS8W5B_M	www.theargus.co.uk	2014-05-13 15:47:37	1	2014-05-12 16:44:53	en	jailed,pub,milward,stab,murder,man,doorman,hastings,shortly,tried,midnight,wetherspoons,attempted,road,staff	"A man has been jailed for 13 years for the attempted murder of a pub doorman.

Unemployed Michael Barrow, 45, of Milward Road, Hastings, tried to stab a member of door staff at Wetherspoons in Havelock Road shortly before midnight on Saturday July 6 last year."	A man jailed 13 years attempted murder pub doorman Unemployed Michael Barrow, 45, Milward Road, Hastings, tried stab member door staff Wetherspoons Havelock Road shortly midnight Saturday July 6 last year	0	Unemployed Michael Barrow,year,pub doorman,Milward Road,Havelock Road,door staff,murder,Saturday July,Hastings,member,Wetherspoons,midnight	20	Michael	15	Unemployed Michael Barrow,year,pub doorman,Milward Road,Havelock Road,door staff,murder,Saturday July,Hastings,member,Wetherspoons,midnight,Michael	35	a man has been jail for 13 year for the attempt murder of a pub doorman unemploy michael barrow, 45, of milward road, hastings, tri to stab a member of door staff at wetherspoon in havelock road short befor midnight on saturday juli 6 last year	1	a man jail 13 year attempt murder pub doorman unemploy michael barrow, 45, milward road, hastings, tri stab member door staff wetherspoon havelock road short midnight saturday juli 6 last year	1	man jail attempt murder pub doorman unemploy michael barrow milward road hastings tri stab member door staff wetherspoon havelock road short midnight last year	1	a man have be jail for 13 year for the attempt murder of a pub doorman.Unemployed Michael Barrow , 45 , of Milward Road , Hastings , try to stab a member of door staff at Wetherspoons in Havelock Road shortly before midnight on Saturday July 6 last year.	148	a man has been jail for 13 year for the attempt murder of a pub doorman.Unemployed Michael Barrow , 45 , of Milward Road , Hastings , try to stab a member of door staff at Wetherspoons in Havelock Road shortly before midnight on Saturday July 6 last year.	146	man has been jail for for the attempt murder pub doorman unemployed michael barrow milward road hasting try stab member door staff wetherspoon havelock road shortly before midnight last year	146	1	1	0
211340	Alcohol consumption on rise	http://www.indiatvnews.com/news/india/alcohol-consumption-on-rise-36688.html	indiatvnews.com	m	d_fZttD4zTqbgVMwDzj_ZPS8W5B_M	www.indiatvnews.com	2014-05-13 15:47:40	1	2014-05-12 22:30:00	en	consumption,sorry,region,inconvenience,restricted,rise,alcohol,visiting,tvwe,india,thanks,service	"Thanks for visiting India TV

We have restricted our service in your region for the time being. Sorry for the inconvenience."	Thanks visiting India TV We restricted service region time Sorry inconvenience	0	India TV,time,sorry,region,inconvenience,service,thank	15	empty	10	India TV,time,sorry,region,inconvenience,service,thank,empty	25	thank for visit india tv we have restrict our servic in your region for the time be sorri for the inconveni	1	thank visit india tv we restrict servic region time sorri inconveni	0	thank visit india restrict servic region sorri inconveni	0	"thank for visit India TV 

 we have restrict our service in your region for the time be.sorry for the inconvenience."	140	"thank for visit India TV 

 we have restrict our service in your region for the time being.sorry for the inconvenience."	139	thank for visit india have restrict our service your region for the being sorry for the inconvenience	139	1	1	0
265476	Actors find common ground in 'A Million Ways to Die in the West'	http://www.news-record.com/go_triad/article_25f1d9b0-e6dd-11e3-8ebc-001a4bcf6878.html	Greensboro News \& Record	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	www.news-record.com	2014-05-29 14:10:30	1		en	west,digital,ways,zip,die,sorry,million,ground,deliverable,zipcode,code,actors,sign,servicereenter,common,area,subscription	"Sorry, this zipcode is not in our deliverable area for this subscription service.

Re-enter zip code or sign up for digital access.

Get digital access"	Sorry, zipcode deliverable area subscription service Re-enter zip code sign digital access Get digital access	0	digital access,zip code,subscription service,deliverable area,zipcode	15	empty	12	digital access,zip code,subscription service,deliverable area,zipcode,empty	27	sorry, this zipcod is not in our deliver area for this subscript servic re-ent zip code or sign up for digit access get digit access	1	sorry, zipcod deliver area subscript servic re-ent zip code sign digit access get digit access	0	sorry zipcod deliver area subscript servic ent zip code sign digit access get digit access	1	sorry , this zipcode be not in our deliverable area for this subscription service.re - enter zip code or sign up for digital access.Get digital access	150	sorry , this zipcode is not in our deliverable area for this subscription service.re - enter zip code or sign up for digital access.Get digital access	151	sorry this zipcode not our deliverable area for this subscription service enter zip code sign for digital access get digital access	150	1	1	0
265495	In Local Theaters	http://tdn.com/lifestyles/in-local-theaters/article_42da4abe-e6c2-11e3-94f9-0019bb2963f4.html	Longview Daily News	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	tdn.com	2014-05-29 14:10:35	1		en	local,thedaily,email,problem,posts,notificationwhenever,sent,savedthere,notifications,saving,theaters,youll	"Close Get email notifications on TheDaily News daily!

Your notification has been saved.

There was a problem saving your notification.

Whenever TheDaily News posts new content, you'll get an email delivered to your inbox with a link.

Email notifications are only sent once a day, and only if there are new matching items."	Close Get email notifications TheDaily News daily! Your notification saved There problem saving notification Whenever TheDaily News posts new content, get email delivered inbox link Email notifications sent day, new matching items	0	TheDaily News,email notification,new content,notification,email,new matching item,problem,link,inbox,day	21	TheDaily,TheDaily	16	TheDaily News,email notification,new content,notification,email,new matching item,problem,link,inbox,day,TheDaily	37	close get email notif on thedaili news daily! your notif has been save there was a problem save your notif whenev thedaili news post new content, you'll get an email deliv to your inbox with a link email notif are onli sent onc a day, and onli if there are new match item	1	close get email notif thedaili news daily! your notif save there problem save notif whenev thedaili news post new content, get email deliv inbox link email notif sent day, new match item	1	close get email notif thedaili news daily notif save problem save notif whenev thedaili news post new content get email deliv inbox link email notif sent day new match item	1	"close Get email notification on TheDaily News daily ! 

 your notification have be save.there be a problem save your notification.whenever TheDaily News post new content , you will get an email deliver to your inbox with a link.email notification be only send once a day , and only if there be new matching item."	152	"close Get email notification on TheDaily News daily ! 

 your notification has been save.there was a problem save your notification.whenever TheDaily News post new content , you 'll get an email deliver to your inbox with a link.email notification are only send once a day , and only if there are new matching item."	152	close get email notification thedaily news daily your notification has been save there was problem save your notification whenever thedaily news post new content you get email deliver your inbox with link email notification are only send once day and only there are new matching item	217	1	1	0
265496	Charlize Theron says gruelling Mad Max: Fury Road shoot nearly ended her  ...	http://www.news.com.au/entertainment/movies/charlize-theron-says-gruelling-mad-max-fury-road-shoot-nearly-ended-her-career/story-e6frfmw0-1226934444031	NEWS.com.au	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	www.news.com.au	2014-05-29 14:10:36	1			shoot,west,ways,movie,mad,die,road,seth,theron,million,nearly,gruelling,ended,charlize,fury,relationship,film,max	"Watch a clip from the film "A Million Ways to Die in the West." Starring Seth MacFarlane, Charlize Theron, Liam Neeson, Neil Patrick Harris, Amanda Seyfried, and Sarah Silverman. (Photo/Video: Universal)

MAD Max: Fury Road could have been the film that killed Charlize Theron’s career. Or, at least, maimed it for a while.

“It was hard,” she says bluntly when asked about the film, due for release next May.

Picture special: Sexy Charlize Theron

Charlize Theron opens up on relationship with Sean Penn

News_Image_File: Charlize Theron was set to take a break from movies when A Million Ways to Die in the West came along.

“It was physically hard, it was logistically hard, it was long, it was tedious, it was exhausting. It was a difficult movie to make, not because of any one person, not because of the material, it just was a world that was very difficult to integrate into.”

Yet Theron believes some films just have to be like that — “I don’t know if there’s another way to make that movie, you know?” — and that her on-set experience will have little bearing on the end product.

“God no, it doesn’t take away from my belief in the material and George Miller and the cast and Tom Hardy. For me, a huge part of it was that it was so long and I was so far away. I was a new mum and had to move my whole world to Namibia for almost a year, a location where you couldn’t really escape, you were just in it all the time.

News_Image_File: The actress was pictured in Cape Town towards the end of filming for Mad Max: Fury Road. Picture: Esa Alexander / Sunday Times / Gallo Images / Getty Images

“There was an airport that was closed off most of the time. There was no way to get out. Most movies are three/four months — you can endure anything for three/four months. Beyond that, for me, it becomes very hard.”

When she did escape, at the end of 2012, Theron thought it would be best to take a break from acting and spend time with her son, Jackson. She’d adopted him a few months before Namibia; he’s now 2 ½ years old.

“I was going to take time off, I thought that would be the answer. I was like, ‘I don’t have to work. Why am I doing this? I’m a new mum, I should be enjoying this’.”

News_Image_File: Amanda Seyfried, Neil Patrick Harris, Seth MacFarlane and Charlize Theron in a scene from A Million Ways to Die in the West.

But they say a change is as good as a holiday ... just when Theron was ready to shut up shop, along came Seth MacFarlane’s A Million Ways To Die In the West.

Forget shaving your head and fighting for survival in a post-apocalyptic wasteland; this was a wise-ass comedy Western, full of poo and sex jokes and ludicrous bustles.

It was just the shake-up Theron needed; a reminder that she loves her job: “Overall, in every department, I can say I loved making this movie.”

It’s fair to say Theron, who holds dual South African and US citizenship, is not known for comedy. She has serious drama down (North Country, The Road), blockbuster recognition (Snow White and the Huntsman, Prometheus, The Italian Job) cool factor (Young Adult) and an Oscar (Monster). But comedy?

News_Rich_Media: Monster trailer

“It must be the end of the world!” she laughs when one expresses surprise that she is in a movie by the guy behind The Family Guy and Ted.

“I haven’t done what people consider comedies; I’ve done movies that have crossed over genre and I like that — because that to me is life: not everything is just dramatic, not everything is just funny.

News_Image_File: Charlize Theron at this year’s Oscars.

“I was 22 when I did my first Woody Allen movie and I realised, OK, I don’t think of myself as a great joke-teller, but there’s something in playing things honestly.

“Young Adult, when we screened that movie, people would be killing themselves (with laughter). It wasn’t necessarily the most jokey stuff, but the circumstances lent itself to very funny moments.

“I don’t think of it as too much of a shock. We’re in a time where actors are breaking that mould — there are no more just TV actors or just dramatic actors or just comedians; we’re all playing in different wheelhouses.”

Theron is Anna in A Million Ways To Die In the West, a self-sufficient woman who helps MacFarlane’s sad-sack sheep farmer Albert prove a few points to his ex (Amanda Seyfried) and her snooty new beau (Neil Patrick Harris).

Unfortunately for Albert, he doesn’t know Anna’s husband is a feared outlaw (Liam Neeson).

Theron left the poo jokes to Harris: “I would not even try to hold a candle to that,” she says, laughing. What she scored instead was some amazing dialogue about her “smoking hot” self and her “great t---”.

News_Image_File: Charlize Theron says she and Seth MacFarlane shared a lot of laughs on A Million Ways To Die in the West.

“My God did I give Seth a lot of s--- for that,” she says. “Things like that, your ego could step in and you could get embarrassed about it, but then you realise the shocking aspect makes it funny.

“I wouldn’t have been brave enough to ever try that on a guy,” she adds with a laugh, “but now I just walk around talking about my t--- all the time.”

Well, Charlize Theron saying “I’ve got great t---” is funny because it’s true, right?

“No,” she laughs, “it’s so not!”

MacFarlane had Theron watch Defending Your Life as research: “An Albert Brooks film with Meryl Streep,” she explains. “In that relationship, Albert would make Meryl laugh and it was infectious: the more she laughed, the more you wanted to laugh.”

News_Image_File: Charlize Theron plays Charades during an appearance on The Tonight Show Starring Jimmy Fallon this month.

She and MacFarlane laugh a lot in A Million Ways To Die In the West. And not just aided by pot cookies, as in one scene. (“I haven’t smoked pot in forever,” says Theron. “When I do it I fall asleep and that’s no fun. But I’m all for pot. I love pot heads!”)

That laughter fits with what Theron saw as her job on West: grounding the nutty goings-on in reality.

And in reality, she says, laughter “is what most relationships are built on”.

She wasn’t supposed to laugh in her scenes with Neeson — including one where he slaps her — but couldn’t help herself.

“I remember not being able to get through that with a straight face. Seth finally came up to me and he was like, ‘It’s starting to look like you like being hit and that’s not good’.”

News_Image_File: Charlize Theron and Sean Penn at the world premiere of A Million Ways To Die In The West.

Theron, 38, arrived at the A Million Ways To Die In the West premiere on the arm of her boyfriend, Sean Penn. While they’ve gone red-carpet public, Theron remains reluctant to discuss the relationship; she has a standard line about being “not good at talking about that stuff”.

Theron and Penn, 53, have been friends for a long time, their relationship built not just on laughter but their shared passion for activism — she as a UN Messenger of Peace and on issues such as HIV prevention and animal cruelty; he in bringing aid to disaster zones such as New Orleans and Haiti.

Asked by US TV host Matt Lauer last week about their relationship evolving into something more, Theron said: “If you have that kind of enduring friendship like we did, you value it and you don’t want to just make an impulsive decision that can damage that.”

Her personal life going well and love of her job restored, Theron’s focus will later this year turn to another project with an Australian connection: she will produce and star in the indie film American Express, to be directed by Nash Edgerton. “I’m so in love with that script,” she says."																					1	0	0
265499	Seth MacFarlane Is Not Hollywood's Next Great Leading Man	http://www.buzzfeed.com/alisonwillmore/seth-macfarlane-is-not-hollywoods-next-great-leading-man	BuzzFeed	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	www.buzzfeed.com	2014-05-29 14:10:36	1		en	hollywoods,west,ways,die,leading,seth,million,theron,albert,man,hes,macfarlanes,comedy,macfarlane,great	"Universal Pictures Charlize Theron and Seth MacFarlane in A Million Ways to Die in the West

It's been a long, snaky road from animator to star for Seth MacFarlane, but he's finally made it with A Million Ways to Die in the West, the Western comedy he co-wrote and directed that opens in theaters this Friday. The film features the Family Guy creator in his first live-action leading role as Albert, a cowardly sheep farmer living in Arizona in 1882 — a development the world may not have been waiting on anxiously, but MacFarlane sure seems to have been. The massively successful TV producer has always shown an urge to perform, even as he's built an animated empire over the course of the last decade. MacFarlane's voiced major characters in all of his animated series, including Peter, Brian, and Stewie Griffin, as well as the titular teddy bear in his movie directorial debut Ted. He's also recorded albums of swing and jazz standards and hosted Saturday Night Live, Comedy Central roasts, and a particularly divisive Academy Awards. When it comes to television, MacFarlane's (in)famous for quick cutaways and shock comedy in which no subject is safe. But in edging his way onto the screen himself in A Million Ways to Die in the West, he tries to balance the expected jokes about race, bodily fluids, and child brides with some actual romance. The animator-turned-actor may like pushing buttons, but in the end, he just wants to be loved.

Lorey Sebastian/Universal Pictures

The thing is, love or hate MacFarlane's brand of humor, his smug, brotastic persona is basically the opposite of lovable. In A Million Ways to Die in the West, it's a giant, self-created obstacle he doesn't manage to overcome. Whatever he might be like in person, MacFarlane's cultivated a permasmirk in public that serves as a pre-emptive response to anyone who dares get offended by one of his gags — like the one at the Oscars when he opened the night by singing that awful two-minute ode to seeing actresses' boobs, all in the guise of a slight against himself. (The joke is that it's an offensive joke, y'all!) MacFarlane's a huge Hollywood success who heads up a billion-dollar franchise and has dated a string of starlets, but in A Million Ways to Die in the West, he's cast himself as a nice but weak-kneed type, a self-proclaimed nerd who gets dumped by his girlfriend Louise (Amanda Seyfried) and requires multiple pep talks about how great he really is from his love interest Anna (Charlize Theron). It's a jarring contrast, given the degree to which the movie's set up to not require him to act but to just be himself, with anachronistic, self-aware dialogue. (At one point, Albert notes he's not the hero; "I'm the guy in the crowd making fun of the hero's shirt.") A Million Ways to Die in the West suggests that, like fellow multihyphenate Kevin Smith, MacFarlane still sees himself as the scrappy underdog while, to much of the outside world, he looks more like the occasional bully.

Universal Pictures Amanda Seyfried and Neil Patrick Harris

Co-written by regular MacFarlane collaborators Alec Sulkin and Wellesley Wild, A Million Ways to Die in the West is an unhurried combination of the expected sort of gags (a character takes a prolonged shit into a hat, there are some random celebrity cameos, and half-hearted jabs at Native Americans, Jews, and Muslims) and some woefully flat attempts at actual character development for Albert. But MacFarlane has surrounded himself with some great talent, so the movie chugs along anyway, even when its jokes fail to land. Neil Patrick Harris, who plays a monied storeowner, could wring laughs from a Holocaust joke (and practically has to), while Sarah Silverman brings an R-rated chipperness to her role as a hooker who, in her personal life, is saving herself for marriage to boyfriend Edward (Giovanni Ribisi). But it's Charlize Theron who gives the most warm, comfortable, enthusiastic performance in between the bits about the jizz stuck to the side of a prostitute's face and the "runaway slave"-themed shooting gallery at the fair. She's playing a period piece cool girl, but in scenes in which she gives Albert a hard time about his hesitation in eating a pot cookie or jokes about the discomfort of her evening dress's bustle, she encapsulates the tone the movie aims for and fails to hit. She's unabashedly contemporary and down-to-earth while committing to a character who's secretly the wife of an outlaw (Liam Neeson). For an actress who's so often cast as regal or imperious, she's wonderfully at ease in this comedy — more so than her co-star.

Universal Pictures Giovanni Ribisi and Sarah Silverman"																					1	0	0
265503	Now showing: 'Maleficent,' 'Million Ways to Die in the West' open Friday at Staten  ...	http://www.silive.com/entertainment/tvfilm/index.ssf/2014/05/post_137.html	SILive.com	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	www.silive.com	2014-05-29 14:10:38	1	2014-05-28 17:19:41	en	movie,language,maleficent,stars,pg13,min,staten,west,ways,nudity,film,island,theaters,showing,pg,half,violence,million,open	"STAR RATINGS KEY: FOUR STARS = Excellent. THREE STARS: Good. TWO STARS: Fair. ONE STAR: Poor. ZERO STARS: Bomb.

STATEN ISLAND, N.Y. — Capsule reviews of the major film releases now showing borough theaters, courtesy of film critic Stephen Whitty:

NEW THIS WEEK: OPENING MAY 30:

"MALEFICENT" A beautiful, pure-hearted young woman, Maleficent, has an idyllic life growing up in a peaceable forest kingdom, until one day when an invading army threatens the harmony of the land. Maleficent rises to be the land's fiercest protector (Angelina Jolie), but she ultimately suffers a ruthless betrayal-an act that begins to turn her pure heart to stone. Bent on revenge, Maleficent faces an epic battle with the invading king's successor and, as a result, places a curse upon his newborn infant Aurora (Dakota Fanning). As the child grows, Maleficent realizes that Aurora holds the key to peace in the kingdom — and perhaps to Maleficent's true happiness as well. PG for scares. 135 min.

"A MILLION WAYS TO DIE IN THE WEST" A very vulgar (and often funny) Western spoof from Seth MacFarlane, with the button-eyed comic as the reluctant hero in a story of gold, gunslingers and sheep. MacFarlane isn't a natural movie star, but Charlize Theron, Liam Neeson, Neil Patrick Harris and Sarah Silverman are there to help out, the many of the jokes are good, albeit guiltlessly raunchy. It's no "Blazing Saddles" but it's in the same wagon train. R for strong language, sexual situations, brief nudity, substance abuse and violence. 116 min. THREE STARS

ALSO OUT NOW:

"THE AMAZING SPIDER-MAN 2" The latest superhero sequel is, strangely,

better on character than on spectacle, with a nice romance between

Spidey and Gwen (real-life lovers Andrew Garfield and Emma Stone) but

a pretty rote plot full of hollow action; it's a comic-book movie that

seems to wish it was something else. PG-13 for violence. 142 min.

TWO & A HALF STARS



"BLENDED" After a disastrous blind date, single parents Lauren (Drew Barrymore) and Jim (Adam Sandler) agree on only one thing: they never want to see each other again. But when they each sign up separately for a fabulous family vacation with their kids, they're all stuck sharing a suite at a luxurious African safari resort for a week. PG-13 for language and crude humor. 117 min. NS



"CAPTAIN AMERICA: WINTER SOLDIER" A very solid sequel to Marvel's

red-white-and-blue war hero, now part of our modern superhero age,

with the hunky (albeit slightly dull) Chris Evans and the terrific

Scarlett Johansson confronting plots, traitors and old enemies.

Terrific action, and some surprising guest stars (Robert Redford and

Samuel L. Jackson), but a little too much reliance on knives, guns and

assault weapons; these movies are best when they're an escape from

real life, not a reminder of it. PG-13 for violence. 136 min. THREE STARS



"FADING GIGOLO" Fioravante (John Turturro) decides to become a

professional Don Juan as a way of making money to help his

cash-strapped friend, Murray (Woody Allen). With Murray acting as his

"manager", the duo quickly finds themselves caught up in the

crosscurrents of love and money. Sofia Vergara and Sharon Stone

co-star. R for language and brief nudity. 90 min.THREE STARS

"GODZILLA" Basically a '60s kiddie matinee, but with real effects

instead of a guy in a rubber suit, and a strange number of real actors

(Bryan Cranston? Juliette Binoche?) picking up paychecks. It's fun

when, about halfway through, Godzilla starts beating up on two other

monsters, but really this is just junk food and eye candy. PG-13 for

violence. 123 min. TWO & A HALF STARS

"HEAVEN IS FOR REAL" Todd Burpo (Greg Kinnear) and Sonja Burpo (Kelly

Reilly) are the real-life couple whose son Colton claims to have

visited Heaven during a near death experience. Colton recounts the

details of his amazing journey with childlike innocence and speaks

matter-of-factly about things that happened before his birth ...

things he couldn't possibly know. Todd and his family are then

challenged to examine the meaning from this remarkable event. PG for

some medical situations and brief language. 110 min. NS



"LEGEND OF OZ: DOROTHY RETURN" Yet another sequel to the story we all

know, this one based on a new series by L. Frank Baum's great-grandson

which brings back a few familiar characters, adds some new ones — and

yet never comes close to recapturing the magic. Fairly cheap-looking,

even in 3D, only the hard work of Martin Short (who, btw, is appearing

May 17 at the St. George Theatre — here voicing the Jester, the

villainous brother of the Wicked Witch — makes it tolerable. PG for

some scary scenes. 88 min. TWO STARS

"MILLION DOLLAR ARM" Another in the inspiring sports-movie genre, this

one about two against-all-odd prospects from India that sports agent

Jon Hamm tries to turn into major leaguers. The actors work hard, but

there's a taint of condescension to the film's portrayal of its

minority characters, and the plotting is purely predictable. PG for

some alcohol abuse. 124 min. TWO & A HALF STARS

"NEIGHBORS" When a noisy fraternity moves in next door to a couple of new parents, the stage is set for a lot of noisy conflicts, and eventually war. But appealing as stars Seth Rogen, Zac Efron and Rose Byrne are, the movie is a little too single-mindedly raunchy, and passes up the chance to do more than sex an drug jokes, or develop any of its supporting characters. R for nudity, sexual situations, substance abuse, violence and strong language. 96 min. TWO & A HALF STARS

"RIO 2" There are no princesses in "Rio 2." No superheroes. No talking

Legos. No plush talking puppets. No sarcastic double entendres. The

follow-up to 2011's animated "Rio" is, simply put, a highly

entertaining old-fashioned family film – albeit lushly rendered in

3-D. G. 101 min. THREE STARS

"X-MEN: DAYS OF FUTURE PAST" The seventh (!) "X-Men" film turns out to be one of the best, as the casts of both series team up for a bit of time travel (and a lot of special-effects eye candy.) It's overstuffed (and for purely casual fans, overcomplicated) but Hugh Jackman and Jennifer Laurence remain terrific, and James McAvoy and Michael Fassbender strike sparks. PG-13 for violence and brief nudity. 131 min. THREE STARS"	STAR RATINGS KEY: FOUR STARS = Excellent THREE STARS: Good TWO STARS: Fair ONE STAR: Poor ZERO STARS: Bomb STATEN ISLAND, N Y — Capsule reviews major film releases showing borough theaters, courtesy film critic Stephen Whitty: NEW THIS WEEK: OPENING MAY 30: "MALEFICENT" A beautiful, pure-hearted young woman, Maleficent, idyllic life growing peaceable forest kingdom, one day invading army threatens harmony land Maleficent rises land's fiercest protector (Angelina Jolie), ultimately suffers ruthless betrayal-an act begins turn pure heart stone Bent revenge, Maleficent faces epic battle invading king's successor and, result, places curse upon newborn infant Aurora (Dakota Fanning) As child grows, Maleficent realizes Aurora holds key peace kingdom — perhaps Maleficent's true happiness well PG scares 135 min "A MILLION WAYS TO DIE IN THE WEST" A vulgar (and often funny) Western spoof Seth MacFarlane, button-eyed comic reluctant hero story gold, gunslingers sheep MacFarlane natural movie star, Charlize Theron, Liam Neeson, Neil Patrick Harris Sarah Silverman help out, many jokes good, albeit guiltlessly raunchy It's "Blazing Saddles" wagon train R strong language, sexual situations, brief nudity, substance abuse violence 116 min THREE STARS ALSO OUT NOW: "THE AMAZING SPIDER-MAN 2" The latest superhero sequel is, strangely, better character spectacle, nice romance Spidey Gwen (real-life lovers Andrew Garfield Emma Stone) pretty rote plot full hollow action; comic-book movie seems wish something else PG-13 violence 142 min TWO & A HALF STARS "BLENDED" After disastrous blind date, single parents Lauren (Drew Barrymore) Jim (Adam Sandler) agree one thing: never want see But sign separately fabulous family vacation kids, they're stuck sharing suite luxurious African safari resort week PG-13 language crude humor 117 min NS "CAPTAIN AMERICA: WINTER SOLDIER" A solid sequel Marvel's red-white-and-blue war hero, part modern superhero age, hunky (albeit slightly dull) Chris Evans terrific Scarlett Johansson confronting plots, traitors old enemies Terrific action, surprising guest stars (Robert Redford Samuel L Jackson), little much reliance knives, guns assault weapons; movies best they're escape real life, reminder PG-13 violence 136 min THREE STARS "FADING GIGOLO" Fioravante (John Turturro) decides become professional Don Juan way making money help cash-strapped friend, Murray (Woody Allen) With Murray acting "manager", duo quickly finds caught crosscurrents love money Sofia Vergara Sharon Stone co-star R language brief nudity 90 min THREE STARS "GODZILLA" Basically '60s kiddie matinee, real effects instead guy rubber suit, strange number real actors (Bryan Cranston? Juliette Binoche?) picking paychecks It's fun when, halfway through, Godzilla starts beating two monsters, really junk food eye candy PG-13 violence 123 min TWO & A HALF STARS "HEAVEN IS FOR REAL" Todd Burpo (Greg Kinnear) Sonja Burpo (Kelly Reilly) real-life couple whose son Colton claims visited Heaven near death experience Colton recounts details amazing journey childlike innocence speaks matter-of-factly things happened birth things possibly know Todd family challenged examine meaning remarkable event PG medical situations brief language 110 min NS "LEGEND OF OZ: DOROTHY RETURN" Yet another sequel story know, one based new series L Frank Baum's great-grandson brings back familiar characters, adds new ones — yet never comes close recapturing magic Fairly cheap-looking, even 3D, hard work Martin Short (who, btw, appearing May 17 St George Theatre — voicing Jester, villainous brother Wicked Witch — makes tolerable PG scary scenes 88 min TWO STARS "MILLION DOLLAR ARM" Another inspiring sports-movie genre, one two against-all-odd prospects India sports agent Jon Hamm tries turn major leaguers The actors work hard, there's taint condescension film's portrayal minority characters, plotting purely predictable PG alcohol abuse 124 min TWO & A HALF STARS "NEIGHBORS" When noisy fraternity moves next door couple new parents, stage set lot noisy conflicts, eventually war But appealing stars Seth Rogen, Zac Efron Rose Byrne are, movie little single-mindedly raunchy, passes chance sex drug jokes, develop supporting characters R nudity, sexual situations, substance abuse, violence strong language 96 min TWO & A HALF STARS "RIO 2" There princesses "Rio 2 " No superheroes No talking Legos No plush talking puppets No sarcastic double entendres The follow-up 2011's animated "Rio" is, simply put, highly entertaining old-fashioned family film – albeit lushly rendered 3-D G 101 min THREE STARS "X-MEN: DAYS OF FUTURE PAST" The seventh (!) "X-Men" film turns one best, casts series team bit time travel (and lot special-effects eye candy ) It's overstuffed (and purely casual fans, overcomplicated) Hugh Jackman Jennifer Laurence remain terrific, James McAvoy Michael Fassbender strike sparks PG-13 violence brief nudity 131 min THREE STARS	3	star,half STARS,brief nudity,STARS,substance abuse,strong language,sexual situation,min,good,life,film,eye candy,Maleficent,real,movie,violence,key,week,major,sequel,pg-13,language,way,character,day,superhero,story,comic,pure,thing,kingdom,Seth,amazing,Stone,land,raunchy,plot,action,joke,family,MacFarlane,terrific,Aurora,NS,parent,Excellent,L.,war,fair,rating,poor,little,release,forest,peaceable,army,harmony,money,theater,borough,opening,Murray,bomb,courtesy,Whitty,idyllic,Stephen,critic,Jolie,protector,Angelina,fiercest,NEW,woman,young,ISLAND,STATEN,hearted,MALEFICENT,betrayal,New York,ruthless,beautiful,review,Capsule,Silverman,Harris,Sarah,Patrick,situation,Neeson,brief,Theron,Garfield,Neil,Andrew,Liam,Charlize,Emma,lover	616	Fair,Stephen,Maleficent,Maleficent,Angelina,Maleficent,Aurora,Dakota,Maleficent,Aurora,Maleficent,Seth,MacFarlane,Charlize,Liam,Neil,Sarah,Gwen,Andrew,Emma,Lauren,Jim,Adam,Marvel,Chris,Scarlett,Robert,Samuel,Fioravante,John,Don,Murray,Woody,Murray,Sofia,Sharon,Bryan,Juliette,Godzilla,Todd,Greg,Sonja,Kelly,Colton,Colton,Todd,L.,Martin,Jester,Wicked,Seth,Zac,Rose,Hugh,Jennifer,James,Michael	177	star,half STARS,brief nudity,STARS,substance abuse,strong language,sexual situation,min,good,life,film,eye candy,Maleficent,real,movie,violence,key,week,major,sequel,pg-13,language,way,character,day,superhero,story,comic,pure,thing,kingdom,Seth,amazing,Stone,land,raunchy,plot,action,joke,family,MacFarlane,terrific,Aurora,NS,parent,Excellent,L.,war,fair,rating,poor,little,release,forest,peaceable,army,harmony,money,theater,borough,opening,Murray,bomb,courtesy,Whitty,idyllic,Stephen,critic,Jolie,protector,Angelina,fiercest,NEW,woman,young,ISLAND,STATEN,hearted,MALEFICENT,betrayal,New York,ruthless,beautiful,review,Capsule,Silverman,Harris,Sarah,Patrick,situation,Neeson,brief,Theron,Garfield,Neil,Andrew,Liam,Charlize,Emma,lover,Fair,Dakota,Gwen,Lauren,Jim,Adam,Marvel,Chris,Scarlett,Robert,Samuel,Fioravante,John,Don,Woody,Sofia,Sharon,Bryan,Juliette,Godzilla,Todd,Greg,Sonja,Kelly,Colton,Martin,Jester,Wicked,Zac,Rose,Hugh,Jennifer,James,Michael	793	star rate key: four star = excel three stars: good two stars: fair one star: poor zero stars: bomb staten island, n y — capsul review of the major film releas now show borough theaters, courtesi of film critic stephen whitty: new this week: open may 30: "maleficent" a beautiful, pure-heart young woman, maleficent, has an idyl life grow up in a peaceabl forest kingdom, until one day when an invad armi threaten the harmoni of the land malefic rise to be the land fiercest protector (angelina jolie), but she ultim suffer a ruthless betrayal-an act that begin to turn her pure heart to stone bent on revenge, malefic face an epic battl with the invad king successor and, as a result, place a curs upon his newborn infant aurora (dakota fanning) as the child grows, malefic realiz that aurora hold the key to peac in the kingdom — and perhap to malefic true happi as well pg for scare 135 min "a million way to die in the west" a veri vulgar (and often funny) western spoof from seth macfarlane, with the button-ey comic as the reluct hero in a stori of gold, gunsling and sheep macfarlan isn't a natur movi star, but charliz theron, liam neeson, neil patrick harri and sarah silverman are there to help out, the mani of the joke are good, albeit guiltless raunchi it no "blaze saddles" but it in the same wagon train r for strong language, sexual situations, brief nudity, substanc abus and violenc 116 min three star also out now: "the amaz spider-man 2" the latest superhero sequel is, strangely, better on charact than on spectacle, with a nice romanc between spidey and gwen (real-lif lover andrew garfield and emma stone) but a pretti rote plot full of hollow action; it a comic-book movi that seem to wish it was someth els pg-13 for violenc 142 min two & a half star "blended" after a disastr blind date, singl parent lauren (drew barrymore) and jim (adam sandler) agre on onli one thing: they never want to see each other again but when they each sign up separ for a fabul famili vacat with their kids, they'r all stuck share a suit at a luxuri african safari resort for a week pg-13 for languag and crude humor 117 min ns "captain america: winter soldier" a veri solid sequel to marvel red-white-and-blu war hero, now part of our modern superhero age, with the hunki (albeit slight dull) chris evan and the terrif scarlett johansson confront plots, traitor and old enemi terrif action, and some surpris guest star (robert redford and samuel l jackson), but a littl too much relianc on knives, gun and assault weapons; these movi are best when they'r an escap from real life, not a remind of it pg-13 for violenc 136 min three star "fade gigolo" fioravant (john turturro) decid to becom a profession don juan as a way of make money to help his cash-strap friend, murray (woodi allen) with murray act as his "manager", the duo quick find themselv caught up in the crosscurr of love and money sofia vergara and sharon stone co-star r for languag and brief nuditi 90 min three star "godzilla" basic a 60s kiddi matinee, but with real effect instead of a guy in a rubber suit, and a strang number of real actor (bryan cranston? juliett binoche?) pick up paycheck it fun when, about halfway through, godzilla start beat up on two other monsters, but realli this is just junk food and eye candi pg-13 for violenc 123 min two & a half star "heaven is for real" todd burpo (greg kinnear) and sonja burpo (kelli reilly) are the real-lif coupl whose son colton claim to have visit heaven dure a near death experi colton recount the detail of his amaz journey with childlik innoc and speak matter-of-fact about thing that happen befor his birth thing he couldn't possibl know todd and his famili are then challeng to examin the mean from this remark event pg for some medic situat and brief languag 110 min ns "legend of oz: dorothi return" yet anoth sequel to the stori we all know, this one base on a new seri by l frank baum great-grandson which bring back a few familiar characters, add some new one — and yet never come close to recaptur the magic fair cheap-looking, even in 3d, onli the hard work of martin short (who, btw, is appear may 17 at the st georg theatr — here voic the jester, the villain brother of the wick witch — make it toler pg for some scari scene 88 min two star "million dollar arm" anoth in the inspir sports-movi genre, this one about two against-all-odd prospect from india that sport agent jon hamm tri to turn into major leaguer the actor work hard, but there a taint of condescens to the film portray of it minor characters, and the plot is pure predict pg for some alcohol abus 124 min two & a half star "neighbors" when a noisi fratern move in next door to a coupl of new parents, the stage is set for a lot of noisi conflicts, and eventu war but appeal as star seth rogen, zac efron and rose byrn are, the movi is a littl too single-mind raunchy, and pass up the chanc to do more than sex an drug jokes, or develop ani of it support charact r for nudity, sexual situations, substanc abuse, violenc and strong languag 96 min two & a half star "rio 2" there are no princess in "rio 2 " no superhero no talk lego no plush talk puppet no sarcast doubl entendr the follow-up to 2011 anim "rio" is, simpli put, a high entertain old-fashion famili film – albeit lush render in 3-d g 101 min three star "x-men: day of futur past" the seventh (!) "x-men" film turn out to be one of the best, as the cast of both seri team up for a bit of time travel (and a lot of special-effect eye candi ) it overstuf (and for pure casual fans, overcomplicated) but hugh jackman and jennif laurenc remain terrific, and jame mcavoy and michael fassbend strike spark pg-13 for violenc and brief nuditi 131 min three star	15	star rate key: four star = excel three stars: good two stars: fair one star: poor zero stars: bomb staten island, n y — capsul review major film releas show borough theaters, courtesi film critic stephen whitty: new this week: open may 30: "maleficent" a beautiful, pure-heart young woman, maleficent, idyl life grow peaceabl forest kingdom, one day invad armi threaten harmoni land malefic rise land fiercest protector (angelina jolie), ultim suffer ruthless betrayal-an act begin turn pure heart stone bent revenge, malefic face epic battl invad king successor and, result, place curs upon newborn infant aurora (dakota fanning) as child grows, malefic realiz aurora hold key peac kingdom — perhap malefic true happi well pg scare 135 min "a million way to die in the west" a vulgar (and often funny) western spoof seth macfarlane, button-ey comic reluct hero stori gold, gunsling sheep macfarlan natur movi star, charliz theron, liam neeson, neil patrick harri sarah silverman help out, mani joke good, albeit guiltless raunchi it "blaze saddles" wagon train r strong language, sexual situations, brief nudity, substanc abus violenc 116 min three star also out now: "the amaz spider-man 2" the latest superhero sequel is, strangely, better charact spectacle, nice romanc spidey gwen (real-lif lover andrew garfield emma stone) pretti rote plot full hollow action; comic-book movi seem wish someth els pg-13 violenc 142 min two & a half star "blended" after disastr blind date, singl parent lauren (drew barrymore) jim (adam sandler) agre one thing: never want see but sign separ fabul famili vacat kids, they'r stuck share suit luxuri african safari resort week pg-13 languag crude humor 117 min ns "captain america: winter soldier" a solid sequel marvel red-white-and-blu war hero, part modern superhero age, hunki (albeit slight dull) chris evan terrif scarlett johansson confront plots, traitor old enemi terrif action, surpris guest star (robert redford samuel l jackson), littl much relianc knives, gun assault weapons; movi best they'r escap real life, remind pg-13 violenc 136 min three star "fade gigolo" fioravant (john turturro) decid becom profession don juan way make money help cash-strap friend, murray (woodi allen) with murray act "manager", duo quick find caught crosscurr love money sofia vergara sharon stone co-star r languag brief nuditi 90 min three star "godzilla" basic 60s kiddi matinee, real effect instead guy rubber suit, strang number real actor (bryan cranston? juliett binoche?) pick paycheck it fun when, halfway through, godzilla start beat two monsters, realli junk food eye candi pg-13 violenc 123 min two & a half star "heaven is for real" todd burpo (greg kinnear) sonja burpo (kelli reilly) real-lif coupl whose son colton claim visit heaven near death experi colton recount detail amaz journey childlik innoc speak matter-of-fact thing happen birth thing possibl know todd famili challeng examin mean remark event pg medic situat brief languag 110 min ns "legend of oz: dorothi return" yet anoth sequel stori know, one base new seri l frank baum great-grandson bring back familiar characters, add new one — yet never come close recaptur magic fair cheap-looking, even 3d, hard work martin short (who, btw, appear may 17 st georg theatr — voic jester, villain brother wick witch — make toler pg scari scene 88 min two star "million dollar arm" anoth inspir sports-movi genre, one two against-all-odd prospect india sport agent jon hamm tri turn major leaguer the actor work hard, there taint condescens film portray minor characters, plot pure predict pg alcohol abus 124 min two & a half star "neighbors" when noisi fratern move next door coupl new parents, stage set lot noisi conflicts, eventu war but appeal star seth rogen, zac efron rose byrn are, movi littl single-mind raunchy, pass chanc sex drug jokes, develop support charact r nudity, sexual situations, substanc abuse, violenc strong languag 96 min two & a half star "rio 2" there princess "rio 2 " no superhero no talk lego no plush talk puppet no sarcast doubl entendr the follow-up 2011 anim "rio" is, simpli put, high entertain old-fashion famili film – albeit lush render 3-d g 101 min three star "x-men: day of futur past" the seventh (!) "x-men" film turn one best, cast seri team bit time travel (and lot special-effect eye candi ) it overstuf (and pure casual fans, overcomplicated) hugh jackman jennif laurenc remain terrific, jame mcavoy michael fassbend strike spark pg-13 violenc brief nuditi 131 min three star	14	star rate key four star excel three stars good two stars fair one star poor zero stars bomb staten island capsul review major film releas show borough theaters courtesi film critic stephen whitty new week open maleficent beautiful pure heart young woman maleficent idyl life grow peaceabl forest kingdom one invad armi threaten harmoni land malefic rise land fiercest protector angelina jolie ultim suffer ruthless betrayal act begin turn pure heart stone bent revenge malefic face epic battl invad king successor and result place curs upon newborn infant aurora dakota fanning child grows malefic realiz aurora hold key peac kingdom perhap malefic true happi well scare min million way die west vulgar and often funny western spoof seth macfarlane button comic reluct hero gold gunsling sheep macfarlan natur movi star charliz theron liam neeson neil patrick harri sarah silverman help out mani joke good albeit guiltless raunchi blaze saddles wagon train strong language sexual situations brief nudity substanc abus violenc min three star also now the amaz spider man latest superhero sequel strangely better charact spectacle nice romanc spidey gwen real lif lover andrew garfield emma stone pretti rote plot full hollow action comic book movi seem wish someth els violenc min two half star blended disastr blind date singl parent lauren drew barrymore jim adam sandler agre one thing never want see sign separ fabul famili vacat kids they stuck share suit luxuri african safari resort week languag crude humor min captain america winter soldier solid sequel marvel red white and blu war hero part modern superhero age hunki albeit slight dull chris evan terrif scarlett johansson confront plots traitor old enemi terrif action surpris guest star robert redford samuel jackson littl much relianc knives gun assault weapons movi best they escap real life remind violenc min three star fade gigolo fioravant john turturro decid becom profession juan way make money help cash strap friend murray woodi allen murray act manager duo quick find caught crosscurr love money sofia vergara sharon stone star languag brief nuditi min three star godzilla basic kiddi matinee real effect instead guy rubber suit strang number real actor bryan cranston juliett binoche pick paycheck fun when halfway through godzilla start beat two monsters realli junk food eye candi violenc min two half star heaven real todd burpo greg kinnear sonja burpo kelli reilly real lif coupl whose son colton claim visit heaven near death experi colton recount detail amaz journey childlik innoc speak matter fact thing happen birth thing possibl know todd famili challeng examin mean remark event medic situat brief languag min legend dorothi return yet anoth sequel know one base new seri frank baum great grandson bring back familiar characters add new one yet never come close recaptur magic fair cheap looking even hard work martin short who btw appear georg theatr voic jester villain brother wick witch make toler scari scene min two star million dollar arm anoth inspir sports movi genre one two against all odd prospect india sport agent jon hamm tri turn major leaguer actor work hard there taint condescens film portray minor characters plot pure predict alcohol abus min two half star neighbors noisi fratern move next door coupl new parents stage set lot noisi conflicts eventu war appeal star seth rogen zac efron rose byrn are movi littl single mind raunchy pass chanc sex drug jokes develop support charact nudity sexual situations substanc abuse violenc strong languag min two half star rio princess rio superhero talk lego plush talk puppet sarcast doubl entendr follow anim rio simpli put high entertain old fashion famili film albeit lush render min three star men futur past seventh men film turn one best cast seri team bit travel and lot special effect eye candi overstuf and pure casual fans overcomplicated hugh jackman jennif laurenc remain terrific jame mcavoy michael fassbend strike spark violenc brief nuditi min three star	15	"STAR RATINGS key : four star = Excellent.three star : good.two star : Fair.one star : Poor.ZERO star : bomb.STATEN ISLAND , N.Y.— capsule review of the major film release now show borough theater , courtesy of film critic Stephen Whitty : 

 NEW this week : opening MAY 30 : 

 " MALEFICENT " a beautiful , pure - hearted young woman , Maleficent , have an idyllic life grow up in a peaceable forest kingdom , until one day when an invade army threaten the harmony of the land.maleficent rise to be the land 's fierce protector ( Angelina Jolie ) , but she ultimately suffer a ruthless betrayal - an act that begin to turn her pure heart to stone.bent on revenge , Maleficent face an epic battle with the invade king 's successor and , as a result , place a curse upon his newborn infant Aurora ( Dakota fan ).As the child grow , Maleficent realize that Aurora hold the key to peace in the kingdom — and perhaps to Maleficent 's true happiness as well.pg for scare.135 min." a million way to die in the WEST " a very vulgar ( and often funny ) western spoof from Seth MacFarlane , with the button - eyed comic as the reluctant hero in a story of gold , gunslinger and sheep.MacFarlane be not a natural movie star , but Charlize Theron , Liam Neeson , Neil Patrick Harris and Sarah Silverman be there to help out , the many of the joke be good , albeit guiltlessly raunchy.it be no " Blazing Saddles " but it be in the same wagon train.r for strong language , sexual situation , brief nudity , substance abuse and violence.116 min.three star 

 also out now : 

 " the amazing SPIDER - man 2 " the late superhero sequel be , strangely , 

 better on character than on spectacle , with a nice romance between 

 Spidey and Gwen ( real - life lover Andrew Garfield and Emma Stone ) but 

 a pretty rote plot full of hollow action ; it be a comic - book movie that 

 seem to wish it be something else.pg-13 for violence.142 min.TWO & a half star 



 " BLENDED " After a disastrous blind date , single parent Lauren ( Drew Barrymore ) and Jim ( Adam Sandler ) agree on only one thing : they never want to see each other again.but when they each sign up separately for a fabulous family vacation with their kid , they be all stuck share a suite at a luxurious african safari resort for a week.PG-13 for language and crude humor.117 min.NS 



 " CAPTAIN AMERICA : winter SOLDIER " a very solid sequel to Marvel 's 

 red - white - and - blue war hero , now part of our modern superhero age , 

 with the hunky ( albeit slightly dull ) Chris Evans and the terrific 

 Scarlett Johansson confront plot , traitor and old enemy.terrific action , and some surprising guest star ( Robert Redford and 

 Samuel L.Jackson ) , but a little too much reliance on knife , gun and 

 assault weapon ; these movie be good when they be an escape from 

 real life , not a reminder of it.pg-13 for violence.136 min.three stars 



 " fading GIGOLO " Fioravante ( John Turturro ) decide to become a 

 professional Don Juan as a way of make money to help his 

 cash - strap friend , Murray ( Woody Allen ).With Murray act as his 

 " manager " , the duo quickly find themselves catch up in the 

 crosscurrent of love and money.Sofia Vergara and Sharon Stone 

 co - star.r for language and brief nudity.90 min.three stars 

 " GODZILLA " basically a ' 60 kiddie matinee , but with real effect 

 instead of a guy in a rubber suit , and a strange number of real actor 

 ( Bryan Cranston ? Juliette Binoche ? ) pick up paycheck.it be fun 

 when , about halfway through , Godzilla start beat up on two other 

 monster , but really this be just junk food and eye candy.PG-13 for 

 violence.123 min.TWO & a half star 

 " HEAVEN be for real " Todd Burpo ( Greg Kinnear ) and Sonja Burpo ( Kelly 

 Reilly ) be the real - life couple whose son Colton claim to have 

 visit Heaven during a near death experience.Colton recount the 

 detail of his amazing journey with childlike innocence and speak 

 matter - of - factly about thing that happen before his birth...thing he could not possibly know.Todd and his family be then 

 challenge to examine the meaning from this remarkable event.PG for 

 some medical situation and brief language.110 min.NS 



 " LEGEND of oz : dorothy RETURN " yet another sequel to the story we all 

 know , this one base on a new series by l.Frank Baum 's great - grandson 

 which bring back a few familiar character , add some new one — and 

 yet never come close to recapture the magic.fairly cheap - look , 

 even in 3d , only the hard work of Martin Short ( who , btw , be appear 

 May 17 at the St.George Theatre — here voice the Jester , the 

 villainous brother of the Wicked Witch — make it tolerable.PG for 

 some scary scene.88 min.two STARS 

 " million dollar ARM " another in the inspiring sport - movie genre , this 

 one about two against - all - odd prospect from India that sport agent 

 Jon Hamm try to turn into major leaguer.the actor work hard , but 

 there be a taint of condescension to the film 's portrayal of its 

 minority character , and the plotting be purely predictable.PG for 

 some alcohol abuse.124 min.TWO & a half star 

 " NEIGHBORS " when a noisy fraternity move in next door to a couple of new parent , the stage be set for a lot of noisy conflict , and eventually war.but appealing as star Seth Rogen , Zac Efron and Rose Byrne be , the movie be a little too single - mindedly raunchy , and pass up the chance to do more than sex an drug joke , or develop any of its support character.r for nudity , sexual situation , substance abuse , violence and strong language.96 min.TWO & a half star 

 " RIO 2 " there be no princess in " rio 2." no superhero.no talk 

 Legos.no plush talking puppet.no sarcastic double entendre.the 

 follow - up to 2011 's animate " Rio " be , simply put , a highly 

 entertain old - fashioned family film – albeit lushly render in 

 3-d.g.101 min.three stars 

 " X - men : day of future past " the seventh ( ! ) " X - men " film turn out to be one of the good , as the cast of both series team up for a bit of time travel ( and a lot of special - effect eye candy.) it be overstuffed ( and for purely casual fan , overcomplicate ) but Hugh Jackman and Jennifer Laurence remain terrific , and James McAvoy and Michael Fassbender strike spark.PG-13 for violence and brief nudity.131 min.three star"	444	"STAR RATINGS key : four star = Excellent.three star : good.two star : Fair.one star : Poor.ZERO star : bomb.STATEN ISLAND , N.Y.— capsule review of the major film release now show borough theater , courtesy of film critic Stephen Whitty : 

 NEW this week : opening MAY 30 : 

 " MALEFICENT " a beautiful , pure - hearted young woman , Maleficent , has an idyllic life grow up in a peaceable forest kingdom , until one day when an invade army threaten the harmony of the land.maleficent rise to be the land 's fierce protector ( Angelina Jolie ) , but she ultimately suffer a ruthless betrayal - an act that begin to turn her pure heart to stone.bent on revenge , Maleficent face an epic battle with the invade king 's successor and , as a result , place a curse upon his newborn infant Aurora ( Dakota fan ).As the child grow , Maleficent realize that Aurora hold the key to peace in the kingdom — and perhaps to Maleficent 's true happiness as well.pg for scare.135 min." a million way to die in the WEST " a very vulgar ( and often funny ) western spoof from Seth MacFarlane , with the button - eyed comic as the reluctant hero in a story of gold , gunslinger and sheep.MacFarlane is n't a natural movie star , but Charlize Theron , Liam Neeson , Neil Patrick Harris and Sarah Silverman are there to help out , the many of the joke are good , albeit guiltlessly raunchy.it 's no " Blazing Saddles " but it 's in the same wagon train.r for strong language , sexual situation , brief nudity , substance abuse and violence.116 min.three star 

 also out now : 

 " the amazing SPIDER - man 2 " the late superhero sequel is , strangely , 

 better on character than on spectacle , with a nice romance between 

 Spidey and Gwen ( real - life lover Andrew Garfield and Emma Stone ) but 

 a pretty rote plot full of hollow action ; it 's a comic - book movie that 

 seem to wish it was something else.pg-13 for violence.142 min.TWO & a half star 



 " BLENDED " After a disastrous blind date , single parent Lauren ( Drew Barrymore ) and Jim ( Adam Sandler ) agree on only one thing : they never want to see each other again.but when they each sign up separately for a fabulous family vacation with their kid , they 're all stuck share a suite at a luxurious african safari resort for a week.PG-13 for language and crude humor.117 min.NS 



 " CAPTAIN AMERICA : winter SOLDIER " a very solid sequel to Marvel 's 

 red - white - and - blue war hero , now part of our modern superhero age , 

 with the hunky ( albeit slightly dull ) Chris Evans and the terrific 

 Scarlett Johansson confront plot , traitor and old enemy.terrific action , and some surprising guest star ( Robert Redford and 

 Samuel L.Jackson ) , but a little too much reliance on knife , gun and 

 assault weapon ; these movie are good when they 're an escape from 

 real life , not a reminder of it.pg-13 for violence.136 min.three stars 



 " fading GIGOLO " Fioravante ( John Turturro ) decide to become a 

 professional Don Juan as a way of make money to help his 

 cash - strap friend , Murray ( Woody Allen ).With Murray act as his 

 " manager " , the duo quickly find themselves catch up in the 

 crosscurrent of love and money.Sofia Vergara and Sharon Stone 

 co - star.r for language and brief nudity.90 min.three stars 

 " GODZILLA " basically a ' 60 kiddie matinee , but with real effect 

 instead of a guy in a rubber suit , and a strange number of real actor 

 ( Bryan Cranston ? Juliette Binoche ? ) pick up paycheck.it 's fun 

 when , about halfway through , Godzilla start beat up on two other 

 monster , but really this is just junk food and eye candy.PG-13 for 

 violence.123 min.TWO & a half star 

 " HEAVEN is for real " Todd Burpo ( Greg Kinnear ) and Sonja Burpo ( Kelly 

 Reilly ) are the real - life couple whose son Colton claim to have 

 visit Heaven during a near death experience.Colton recount the 

 detail of his amazing journey with childlike innocence and speak 

 matter - of - factly about thing that happen before his birth...thing he could n't possibly know.Todd and his family are then 

 challenge to examine the meaning from this remarkable event.PG for 

 some medical situation and brief language.110 min.NS 



 " LEGEND of oz : dorothy RETURN " yet another sequel to the story we all 

 know , this one base on a new series by l.Frank Baum 's great - grandson 

 which bring back a few familiar character , add some new one — and 

 yet never come close to recapture the magic.fairly cheap - look , 

 even in 3d , only the hard work of Martin Short ( who , btw , is appear 

 May 17 at the St.George Theatre — here voice the Jester , the 

 villainous brother of the Wicked Witch — make it tolerable.PG for 

 some scary scene.88 min.two STARS 

 " million dollar ARM " another in the inspiring sport - movie genre , this 

 one about two against - all - odd prospect from India that sport agent 

 Jon Hamm try to turn into major leaguer.the actor work hard , but 

 there 's a taint of condescension to the film 's portrayal of its 

 minority character , and the plotting is purely predictable.PG for 

 some alcohol abuse.124 min.TWO & a half star 

 " NEIGHBORS " when a noisy fraternity move in next door to a couple of new parent , the stage is set for a lot of noisy conflict , and eventually war.but appealing as star Seth Rogen , Zac Efron and Rose Byrne are , the movie is a little too single - mindedly raunchy , and pass up the chance to do more than sex an drug joke , or develop any of its support character.r for nudity , sexual situation , substance abuse , violence and strong language.96 min.TWO & a half star 

 " RIO 2 " there are no princess in " rio 2." no superhero.no talk 

 Legos.no plush talking puppet.no sarcastic double entendre.the 

 follow - up to 2011 's animate " Rio " is , simply put , a highly 

 entertain old - fashioned family film – albeit lushly render in 

 3-d.g.101 min.three stars 

 " X - men : day of future past " the seventh ( ! ) " X - men " film turn out to be one of the good , as the cast of both series team up for a bit of time travel ( and a lot of special - effect eye candy.) it 's overstuffed ( and for purely casual fan , overcomplicate ) but Hugh Jackman and Jennifer Laurence remain terrific , and James McAvoy and Michael Fassbender strike spark.PG-13 for violence and brief nudity.131 min.three star"	370	star rating key four star excellent three star good two star fair one star poor zero star bomb staten island capsule review the major film release show borough theater courtesy film critic stephen whitty new this week open maleficent beautiful pure hearted young woman maleficent has idyllic life grow peaceable forest kingdom until one when invade army threaten the harmony the land maleficent rise the land fierce protector angelina jolie but she ultimately suffer ruthless betrayal act that begin turn her pure heart stone bend revenge maleficent face epic battle with the invade king successor and result place curse upon his newborn infant aurora dakota fan the child grow maleficent realize that aurora hold the key peace the kingdom and perhaps maleficent true happiness well for scare min million way die the west very vulgar and often funny western spoof from seth macfarlane with the button eyed comic the reluctant hero gold gunslinger and sheep macfarlane natural movie star but charlize theron liam neeson neil patrick harris and sarah silverman are there help out the many the joke are good albeit guiltlessly raunchy blaze saddle but the same wagon train for strong language sexual situation brief nudity substance abuse and violence min three star also out now the amazing spider man the late superhero sequel strangely well character than spectacle with nice romance between spidey and gwen real life lover andrew garfield and emma stone but pretty rote plot full hollow action comic book movie that seem wish was something else for violence min two half star blend after disastrous blind date single parent lauren draw barrymore and jim adam sandler agree only one thing they never want see each other again but when they each sign separately for fabulous family vacation with their kid they stick share suite luxurious african safari resort for week for language and crude humor min captain america winter soldier very solid sequel marvel red white and blue war hero part our modern superhero age with the hunky albeit slightly dull chris evan and the terrific scarlett johansson confront plot traitor and old enemy terrific action and some surprising guest star robert redford and samuel jackson but little too much reliance knife gun and assault weapon these movie are good when they escape from real life not reminder for violence min three star fade gigolo fioravante john turturro decide become professional don juan way make money help his cash strap friend murray woody allen with murray act his manager the duo quickly find themselves catch the crosscurrent love and money sofia vergara and sharon stone star for language and brief nudity min three star godzilla basically kiddie matinee but with real effect instead guy rubber suit and strange number real actor bryan cranston juliette binoche pick paycheck fun when about halfway through godzilla start beat two other monster but really this just junk food and eye candy for violence min two half star heaven for real todd burpo greg kinnear and sonja burpo kelly reilly are the real life couple whose son colton claim have visit heaven during near death experience colton recount the detail his amazing journey with childlike innocence and speak matter factly about thing that happen before his birth thing could possibly know todd and his family are then challenge examine the meaning from this remarkable event for some medical situation and brief language min legend dorothy return yet another sequel the know this one base new series frank baum great grandson which bring back few familiar character add some new one and yet never come close recapture the magic fairly cheap look even only the hard work martin short who btw appear the george theatre here voice the jester the villainous brother the wicked witch make tolerable for some scary scene min two star million dollar arm another the inspiring sport movie genre this one about two against all odd prospect from india that sport agent jon hamm try turn into major leaguer the actor work hard but there taint condescension the film portrayal its minority character and the plotting purely predictable for some alcohol abuse min two half star neighbor when noisy fraternity move next door couple new parent the stage set for lot noisy conflict and eventually war but appealing star seth rogen zac efron and rise byrne are the movie little too single mindedly raunchy and pass the chance more than sex drug joke develop any its support character for nudity sexual situation substance abuse violence and strong language min two half star rio there are princess rio superhero talk legos plush talking puppet sarcastic double entendre the follow animate rio simply put highly entertaining old fashioned family film albeit lushly render min three star man future past the seventh man film turn out one the good the cast both series team for bit travel and lot special effect eye candy overstuffed and for purely casual fan overcomplicate but hugh jackman and jennifer laurence remain terrific and jam mcavoy and michael fassbender strike spark for violence and brief nudity min three star	365	1	1	0
265520	Film Clip: 'A Million Ways to Die in the West'	http://live.wsj.com/video/film-clip-a-million-ways-to-die-in-the-west/03627C73-AB29-4716-9FAC-5A625A8436B4.html	Wall Street Journal	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	live.wsj.com	2014-05-29 14:10:43	1		en	west,shoot,ways,die,million,times,tiger,streets,tested,tied,film,transcript,clip,youre,think,thats	"This transcript has been automatically generated and may not be 100% accurate.

I ... I ... T think you're right now ... the dollar was last tested over credo rating and just extend streets route ... that ... streak while you can never find ... where I tied to the Oregon ... I'm not fighting a shooting gallery ... and doesn't want to lose these are full of its ... the Tiger am about to shoot the full load of beer cans ... she ... the ... Ch ... the the the the the ... that's one solely to do is get fully let me shoot sixteen times before he shoots ... than allowed ..."	This transcript automatically generated may 100% accurate I I T think right dollar last tested credo rating extend streets route streak never find I tied Oregon I'm fighting shooting gallery want lose full Tiger shoot full load beer cans Ch that's one solely get fully let shoot sixteen times shoots allowed	1	beer can,credo rating,gallery,load,streak,Tiger,Oregon,street,dollar,accurate,time,transcript	31	empty	24	beer can,credo rating,gallery,load,streak,Tiger,Oregon,street,dollar,accurate,time,transcript,empty	56	this transcript has been automat generat and may not be 100% accur i i t think you'r right now the dollar was last test over credo rate and just extend street rout that streak while you can never find where i tie to the oregon i'm not fight a shoot galleri and doesn't want to lose these are full of it the tiger am about to shoot the full load of beer can she the ch the the the the the that one sole to do is get fulli let me shoot sixteen time befor he shoot than allow	2	this transcript automat generat may 100% accur i i t think right dollar last test credo rate extend street rout streak never find i tie oregon i'm fight shoot galleri want lose full tiger shoot full load beer can ch that one sole get fulli let shoot sixteen time shoot allow	1	transcript automat generat accur think right dollar last test credo rate extend street rout streak never find tie oregon fight shoot galleri want lose full tiger shoot full load beer can that one sole get fulli let shoot sixteen time shoot allow	1	This transcript have be automatically generate and may not be 100 % accurate.i...i...t think you be right now...the dollar be last test over credo rating and just extend street route...that...streak while you can never find...where i tie to the Oregon...i be not fight a shooting gallery...and do not want to lose these be full of its...the Tiger be about to shoot the full load of beer can...she...the...Ch...the the the the the...that be one solely to do be get fully let me shoot sixteen time before he shoot...than allow...	193	This transcript has been automatically generate and may not be 100 % accurate.i...i...t think you 're right now...the dollar was last test over credo rating and just extend street route...that...streak while you can never find...where i tie to the Oregon...i 'm not fight a shooting gallery...and does n't want to lose these are full of its...the Tiger am about to shoot the full load of beer cans...she...the...Ch...the the the the the...that 's one solely to do is get fully let me shoot sixteen time before he shoot...than allow...	192	this transcript has been automatically generate and not accurate think you right the dollar was last test over credo rating and just extend street route that streak while you can never find where tie the oregon not fight shooting gallery and does want lose these are full its the tiger about shoot the full load beer cans she the the the the the the that one solely get fully let shoot sixteen time before shoot than allow	191	1	1	0
265521	'A Million Ways to Die in The West' Can't Reconcile Dumb Comedy with  ...	http://www.thewire.com/entertainment/2014/05/a-million-ways-to-die/371728/	The Wire	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	www.thewire.com	2014-05-29 14:10:44	1		en	west,domestic,ways,movie,die,dumb,reconcile,million,clinch,albert,soon,abuse,anna,character,comedy,cant,violence,girl	"But didn't I know what I was getting into? After all, this is a movie written, directed, and starring man responsible for the "We Saw Your Boobs" Oscar song. His co-writers are responsible for Fox's Dads. Yes, true, it's hard to say I wasn't warned. And for the most part, the depiction of women in the movie is what I would expect from MacFarlane. The plot revolves around MacFarlane's sheep-farmer character, Albert, getting dumped by Amanda Seyfried's Louise, a vapid girl who soon takes up with the mustachioed Foy (Neil Patrick Harris, whose character poops into multiple hats). Albert soon meets Theron's Anna, who is the perfect example of the "Cool Girl" Gillian Flynn describes in Gone Girl. She's a male fantasy: extremely hot and into drinking and shooting and eating pot cookies. She has no tolerance for a silly girl like Louise. She says things like: "Sometimes a girl needs to get a few assholes out of her system before she realizes what a good guy looks like." The good guy, of course, is MacFarlane's character, only he doesn't know she is actually married to a ruthless baddie. When Clinch finds out Anna has kissed another man, he comes to claim his wife, and Albert is forced to battle him to win and save her.

Hence, Anna spends the movie's latter section being victimized by Clinch, briefly escaping to tell Albert that she and Clinch got married when she was 9. There's a series of jokes about this, in which the punchline is ostensibly statutory rape, a subject that manages to get even less funny after watching Clinch batter Anna in such a visceral way.

There's a lot to take issue with in A Million Ways to Die in the West, but as we attempt to engage in a national discussion about the ubiquitous nature of misogyny thanks to #YesAllWomen, the domestic violence in the movie sticks out like a sore thumb. While the movie makes its titular million ways to die in the west somehow fantastical, it allows Clinch's abuse to be troublingly realistic. His violence toward Anna is an anomaly in the movie—it's scary not silly. (It doesn't help that Neeson and Theron are the two least "comedic" actors in the film, making their scenes clash with the dumb comedy all the more starkly.)

It'd be nice — okay, it'd be tolerable — if MacFarlane found a way to comment on this through the rest of the film, but he's not really interested in commenting on this (or anything else, really, save for perhaps diarrhea and Doc Brown). So these scenes of a woman threatened just exist, sadly, disgustingly. Anna needs to be saved by Albert, and Clinch is just an asshole she needed to "get out of her system."

This article is from the archive of our partner The Wire."																					1	0	0
265526	Seth MacFarlane Writes His Own Bad Reviews For "A Million Ways To Die in  ...	http://www.toofab.com/2014/05/28/seth-mcfarlane-trashes-a-million-ways-to-die-in-the-west-jimmy-fallon-video/	TooFab.com	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	www.toofab.com	2014-05-29 14:10:46	1	2014-05-28 00:00:00	en	west,bad,ways,movie,die,reviews,tell,seth,million,western,critics,writes,video,headlines,writers,macfarlane,withseth	"



Is Seth MacFarlane really trashing his own movie?



Well, kind of sort of. The comedian stopped by "The Tonight Show Starring Jimmy Fallon" on Tuesday, where he had prepared some material of the different ways he's expecting critics to pan his Western flick.



Check out the video above to see a few of the hilarious headlines the actor came up with!



Seth also made it clear movie reviewers cannot use any of his clever punchlines for the comedy, too.



"These are headlines that critics cannot use, when they tell us our movie is sh-t," he told Fallon.



With Seth claiming ownership over headlines like "A Million Ways To Die At The Box Office" ... maybe critics will be forced to sing his praises.



What do you think about the "Family Guy" writer's ridiculous reviews? Tell toofab in the comment section below!"	Is Seth MacFarlane really trashing movie? Well, kind sort The comedian stopped "The Tonight Show Starring Jimmy Fallon" Tuesday, prepared material different ways he's expecting critics pan Western flick Check video see hilarious headlines actor came with! Seth also made clear movie reviewers cannot use clever punchlines comedy, "These headlines critics cannot use, tell us movie sh-t," told Fallon With Seth claiming ownership headlines like "A Million Ways To Die At The Box Office" maybe critics forced sing praises What think "Family Guy" writer's ridiculous reviews? Tell toofab comment section below!	1	Tonight Show Starring Jimmy Fallon,clear movie reviewer,Seth,Seth MacFarlane,hilarious headline,western flick,different way,critic,clever punchline,headline,Box Office,actor,video,Family Guy,comedian,material,ridiculous review,Tuesday,comedy,ownership,comment section,Ways,praise,writer,toofab	42	Seth,Jimmy,Seth,Fallon,Seth	32	Tonight Show Starring Jimmy Fallon,clear movie reviewer,Seth,Seth MacFarlane,hilarious headline,western flick,different way,critic,clever punchline,headline,Box Office,actor,video,Family Guy,comedian,material,ridiculous review,Tuesday,comedy,ownership,comment section,Ways,praise,writer,toofab,Jimmy,Fallon	75	is seth macfarlan realli trash his own movie? well, kind of sort of the comedian stop by "the tonight show star jimmi fallon" on tuesday, where he had prepar some materi of the differ way he expect critic to pan his western flick check out the video abov to see a few of the hilari headlin the actor came up with! seth also made it clear movi review cannot use ani of his clever punchlin for the comedy, too "these are headlin that critic cannot use, when they tell us our movi is sh-t," he told fallon with seth claim ownership over headlin like "a million way to die at the box office" mayb critic will be forc to sing his prais what do you think about the "famili guy" writer ridicul reviews? tell toofab in the comment section below!	3	is seth macfarlan realli trash movie? well, kind sort the comedian stop "the tonight show star jimmi fallon" tuesday, prepar materi differ way he expect critic pan western flick check video see hilari headlin actor came with! seth also made clear movi review cannot use clever punchlin comedy, "these headlin critic cannot use, tell us movi sh-t," told fallon with seth claim ownership headlin like "a million way to die at the box office" mayb critic forc sing prais what think "famili guy" writer ridicul reviews? tell toofab comment section below!	2	seth macfarlan realli trash movie well kind sort comedian stop the tonight show star jimmi fallon tuesday prepar materi differ way expect critic pan western flick check video see hilari headlin actor came with seth also made clear movi review cannot use clever punchlin comedy these headlin critic cannot use tell movi told fallon seth claim ownership headlin like million way die box office mayb critic forc sing prais think famili guy writer ridicul reviews tell toofab comment section below	2	"be Seth MacFarlane really trash his own movie ? 



 well , kind of sort of.the comedian stop by " the tonight Show star Jimmy Fallon " on Tuesday , where he have prepare some material of the different way he be expect critic to pan his western flick.check out the video above to see a few of the hilarious headline the actor come up with ! 



 Seth also make it clear movie reviewer can not use any of his clever punchline for the comedy , too." These be headline that critic can not use , when they tell us our movie be sh - t , " he tell Fallon.With Seth claim ownership over headline like " a Million Ways to die At the Box Office "...maybe critic will be force to sing his praise.what do you think about the " Family Guy " writer 's ridiculous review ? tell toofab in the comment section below !"	172	"is Seth MacFarlane really trash his own movie ? 



 well , kind of sort of.the comedian stop by " the tonight Show star Jimmy Fallon " on Tuesday , where he had prepare some material of the different way he 's expect critic to pan his western flick.check out the video above to see a few of the hilarious headline the actor come up with ! 



 Seth also make it clear movie reviewer can not use any of his clever punchline for the comedy , too." These are headline that critic can not use , when they tell us our movie is sh - t , " he tell Fallon.With Seth claim ownership over headline like " a Million Ways to die At the Box Office "...maybe critic will be force to sing his praise.what do you think about the " Family Guy " writer 's ridiculous review ? tell toofab in the comment section below !"	171	seth macfarlane really trash his own movie well kind sort the comedian stop the tonight show star jimmy fallon tuesday where had prepare some material the different way expect critic pan his western flick check out the video above see few the hilarious headline the actor come with seth also make clear movie reviewer can not use any his clever punchline for the comedy too these are headline that critic can not use when they tell our movie tell fallon with seth claim ownership over headline like million way die the box office maybe critic will force sing his praise what you think about the family guy writer ridiculous review tell toofab the comment section below	172	1	1	0
265527	Film Shorts	http://www.fwweekly.com/2014/05/28/film-shorts-114/	FWWeekly	e	d_f9F47Snop-upMoTwX_dPAyr-vPM	www.fwweekly.com	2014-05-29 14:10:46	1	2014-05-28 00:00:00	en	movies,movie,better,shorts,makes,opens,stars,pg13,director,film,comedy	"OPENING: A Million Ways to Die in the West (R) Seth MacFarlane stars in his own comedy as a cowardly farmer who must save his Old West town from a killer (Liam Neeson). Also with Charlize Theron, Neil Patrick Harris, Amanda Seyfried, Sarah Silverman, Giovanni Ribisi, Wes Studi, Gilbert Gottfried, Christopher Lloyd, and Ewan McGregor. (Opens Friday)

Alphaville (NR) Historical re-release of Jean-Luc Godard’s 1965 science-fiction film about an American secret agent (Eddie Constantine) who’s sent to outer space to free a city from its dictator. Also with Anna Karina and Akim Tamiroff. (Opens Friday in Dallas)

Ida (PG-13) Paweł Pawlikowski (My Summer of Love) directs this drama about a 1960s Polish novitiate nun (Agata Trzebuchowska) who is about to take holy orders when she learns a terrible secret about her family. Also with Agata Kulesza, Dawid Ogrodnik, Jerzy Trela, Adam Szyszkowski, Halina Skoczynska, and Joanna Kulig. (Opens Friday in Dallas)

Maleficent (PG) Angelina Jolie stars in this version of the Sleeping Beauty story as the vindictive fairy who curses a princess (Elle Fanning). Also with Sharlto Copley, Lesley Manville, Imelda Staunton, Juno Temple, Sam Riley, Brenton Thwaites, and Kenneth Cranham. (Opens Friday)

NOW PLAYING:

The Amazing Spider-Man 2 (PG-13) Better than the last movie, but everybody here could have been doing something more worthwhile. This overstuffed sequel features Peter Parker (Andrew Garfield) trying to deal with one too many bad guys in Electro (a too cartoonish Jamie Foxx) and the Green Goblin (Dane DeHaan, very well cast), but the real heart is his need to keep Gwen Stacy (Emma Stone) from being hurt by Spider-Man’s enemies. Director Marc Webb keeps aiming for wonder and terror in the big action set pieces and missing; he hits the right notes without understanding the music. He’s much better in the quieter scenes with Peter and Gwen, as Garfield and Stone make a loose and funny couple. This director and these stars should be making the next great heart-melting romantic comedy, not a Spider-Man movie. Maybe the success of this will let that happen. Also with Sally Field, Colm Feore, Campbell Scott, Embeth Davidtz, Felicity Jones, B.J. Novak, Paul Giamatti, and uncredited cameos by Denis Leary and Chris Cooper.

Belle (PG) A movie that would need to exist even if its historical subject had never lived. Gugu Mbatha-Raw plays Dido Elizabeth Belle, an illegitimate child of mixed race who was raised on the English estate of her granduncle (Tom Wilkinson) in the late 18th century and may have influenced some key court rulings against the slave trade. The drama is stilted, and it often feels like director Amma Asante and writer Misan Sagay are checking off boxes with all the racial, class, and gender issues in play here. Still, they find much rewarding material in their heroine’s singular and often uncomfortable social position. At its best, this movie plays like a Jane Austen marriage comedy with race thrown into the mix as a volatile element. It makes this film unique. Also with Sam Reid, Sarah Gadon, Tom Felton, Matthew Goode, Penelope Wilton, Emily Watson, and Miranda Richardson.

Blended (PG-13) Adam Sandler’s latest comedy actually doesn’t suck, which is a step up from his last three live-action movies. He plays a recently widowed father of three girls who buys an unused South African vacation, only to find that he’s stuck there with a mother of two boys (Drew Barrymore) whom he had a bad blind date with. The movie is too long and never ventures far beyond the resort hotel, and it really needed more of Wendi McLendon-Covey as Barrymore’s best friend. Still, the movie is only overtly offensive in spots and has a few decent gags like the one involving parasailing. Also with Bella Thorne, Emma Fuhrmann, Alyvia Alyn Lind, Braxton Beckham, Kyle Red Silverstein, Terry Crews, Zak Henri, Kevin Nealon, Jessica Lowe, Abdoulaye Ngom, Dan Patrick, Shaquille O’Neal, and Joel McHale.

Captain America: The Winter Soldier (PG-13) Definitely better than Captain America’s first outing. Chris Evans returns as the superhero trying to deal with a coup inside SHIELD. The movie’s critique of the contemporary surveillance state doesn’t quite hold together, nor does the flirtatious turn in the character of Black Widow (Scarlett Johansson) make much sense. Yet directors Anthony and Joe Russo do lots of things well, including an assassination attempt on the road against Nick Fury (Samuel L. Jackson) and the chilling casting of Robert Redford as a SHIELD executive with his own agenda. Captain America is still more interesting as a foil to the other Avengers than on his own, but this is a worthy excursion. Also with Anthony Mackie, Cobie Smulders, Sebastian Stan, Emily VanCamp, Dominic Cooper, Toby Jones, Frank Grillo, and Hayley Atwell.

Chef (R) Jon Favreau stars in a not-so-veiled comment on his own filmmaking career as a star chef who restarts his career with a food truck after being fired from a job at an upscale L.A. restaurant. The filmmaker takes way too long to tell his story and doesn’t do well by the women, but he does capture the chaos and sweat and adrenaline of a high-end restaurant kitchen, and the subplot with him finally connecting with his young son (Emjay Anthony) is nicely done. The movie also boasts scrumptious food photography (the dishes were created by Roy Choi), and Favreau obviously has great respect for the care and attention to detail that chefs give to their work. It’s how the movie’s hero finds himself again, and possibly the filmmaker too. Also with John Leguizamo, Bobby Cannavale, Sofia Vergara, Oliver Platt, Amy Sedaris, Scarlett Johansson, Dustin Hoffman, and Robert Downey Jr.

Divergent (PG-13) Ideal viewing if you’re a teenager. For everyone else, not so much. Shailene Woodley stars in this science-fiction adventure as a girl making her way through a dystopian future society divided into factions. This is based on Veronica Roth’s best-selling novel, which makes a neat little metaphor about how teenagers choose cliques to sort themselves out. Too bad neither the book nor the film makes more of it. Director Neil Burger and his writers make hash out of introducing this future world and show little humor or phantasmagoric power. Woodley makes alert little choices, but the whole thing lacks rhythm, and the action sequences aren’t nearly good enough to make up for the flat tone. Also with Theo James, Miles Teller, Jai Courtney, Zoë Kravitz, Ansel Elgort, Ray Stevenson, Maggie Q, Mekhi Phifer, Christian Madsen, Tony Goldwyn, Ashley Judd, and Kate Winslet.

Draft Day (PG-13) Better than Moneyball. Kevin Costner stars in this throwback movie as an embattled Cleveland Browns GM who makes a flurry of trades to get the player he wants during the NFL draft. The NFL trappings make a nice backdrop for a huge cast of sharply written characters who are well-played by both the famous and unknown actors, even if the GM’s personal life is noticeably weaker than the rest of the movie. The film is much better at depicting the behind-the-scenes dealings, and though Costner misses the desperation of a man who knows his dream job is on the line, his underlying coolness helps with a character who keeps his head amid the pressure. His struggle to get the best out of a losing situation is what makes this movie’s end so exhilarating. Also with Jennifer Garner, Denis Leary, Chadwick Boseman, Josh Pence, Frank Langella, Griffin Newman, Brad Henke, W. Earl Brown, Arian Foster, Terry Crews, Tom Welling, Sam Elliott, Sean Combs, Rosanna Arquette, and Ellen Burstyn."	OPENING: A Million Ways Die West (R) Seth MacFarlane stars comedy cowardly farmer must save Old West town killer (Liam Neeson) Also Charlize Theron, Neil Patrick Harris, Amanda Seyfried, Sarah Silverman, Giovanni Ribisi, Wes Studi, Gilbert Gottfried, Christopher Lloyd, Ewan McGregor (Opens Friday) Alphaville (NR) Historical re-release Jean-Luc Godard’s 1965 science-fiction film American secret agent (Eddie Constantine) who’s sent outer space free city dictator Also Anna Karina Akim Tamiroff (Opens Friday Dallas) Ida (PG-13) Paweł Pawlikowski (My Summer Love) directs drama 1960s Polish novitiate nun (Agata Trzebuchowska) take holy orders learns terrible secret family Also Agata Kulesza, Dawid Ogrodnik, Jerzy Trela, Adam Szyszkowski, Halina Skoczynska, Joanna Kulig (Opens Friday Dallas) Maleficent (PG) Angelina Jolie stars version Sleeping Beauty story vindictive fairy curses princess (Elle Fanning) Also Sharlto Copley, Lesley Manville, Imelda Staunton, Juno Temple, Sam Riley, Brenton Thwaites, Kenneth Cranham (Opens Friday) NOW PLAYING: The Amazing Spider-Man 2 (PG-13) Better last movie, everybody could something worthwhile This overstuffed sequel features Peter Parker (Andrew Garfield) trying deal one many bad guys Electro (a cartoonish Jamie Foxx) Green Goblin (Dane DeHaan, well cast), real heart need keep Gwen Stacy (Emma Stone) hurt Spider-Man’s enemies Director Marc Webb keeps aiming wonder terror big action set pieces missing; hits right notes without understanding music He’s much better quieter scenes Peter Gwen, Garfield Stone make loose funny couple This director stars making next great heart-melting romantic comedy, Spider-Man movie Maybe success let happen Also Sally Field, Colm Feore, Campbell Scott, Embeth Davidtz, Felicity Jones, B J Novak, Paul Giamatti, uncredited cameos Denis Leary Chris Cooper Belle (PG) A movie would need exist even historical subject never lived Gugu Mbatha-Raw plays Dido Elizabeth Belle, illegitimate child mixed race raised English estate granduncle (Tom Wilkinson) late 18th century may influenced key court rulings slave trade The drama stilted, often feels like director Amma Asante writer Misan Sagay checking boxes racial, class, gender issues play Still, find much rewarding material heroine’s singular often uncomfortable social position At best, movie plays like Jane Austen marriage comedy race thrown mix volatile element It makes film unique Also Sam Reid, Sarah Gadon, Tom Felton, Matthew Goode, Penelope Wilton, Emily Watson, Miranda Richardson Blended (PG-13) Adam Sandler’s latest comedy actually doesn’t suck, step last three live-action movies He plays recently widowed father three girls buys unused South African vacation, find he’s stuck mother two boys (Drew Barrymore) bad blind date The movie long never ventures far beyond resort hotel, really needed Wendi McLendon-Covey Barrymore’s best friend Still, movie overtly offensive spots decent gags like one involving parasailing Also Bella Thorne, Emma Fuhrmann, Alyvia Alyn Lind, Braxton Beckham, Kyle Red Silverstein, Terry Crews, Zak Henri, Kevin Nealon, Jessica Lowe, Abdoulaye Ngom, Dan Patrick, Shaquille O’Neal, Joel McHale Captain America: The Winter Soldier (PG-13) Definitely better Captain America’s first outing Chris Evans returns superhero trying deal coup inside SHIELD The movie’s critique contemporary surveillance state doesn’t quite hold together, flirtatious turn character Black Widow (Scarlett Johansson) make much sense Yet directors Anthony Joe Russo lots things well, including assassination attempt road Nick Fury (Samuel L Jackson) chilling casting Robert Redford SHIELD executive agenda Captain America still interesting foil Avengers own, worthy excursion Also Anthony Mackie, Cobie Smulders, Sebastian Stan, Emily VanCamp, Dominic Cooper, Toby Jones, Frank Grillo, Hayley Atwell Chef (R) Jon Favreau stars not-so-veiled comment filmmaking career star chef restarts career food truck fired job upscale L A restaurant The filmmaker takes way long tell story doesn’t well women, capture chaos sweat adrenaline high-end restaurant kitchen, subplot finally connecting young son (Emjay Anthony) nicely done The movie also boasts scrumptious food photography (the dishes created Roy Choi), Favreau obviously great respect care attention detail chefs give work It’s movie’s hero finds again, possibly filmmaker Also John Leguizamo, Bobby Cannavale, Sofia Vergara, Oliver Platt, Amy Sedaris, Scarlett Johansson, Dustin Hoffman, Robert Downey Jr Divergent (PG-13) Ideal viewing you’re teenager For everyone else, much Shailene Woodley stars science-fiction adventure girl making way dystopian future society divided factions This based Veronica Roth’s best-selling novel, makes neat little metaphor teenagers choose cliques sort Too bad neither book film makes Director Neil Burger writers make hash introducing future world show little humor phantasmagoric power Woodley makes alert little choices, whole thing lacks rhythm, action sequences aren’t nearly good enough make flat tone Also Theo James, Miles Teller, Jai Courtney, Zoë Kravitz, Ansel Elgort, Ray Stevenson, Maggie Q, Mekhi Phifer, Christian Madsen, Tony Goldwyn, Ashley Judd, Kate Winslet Draft Day (PG-13) Better Moneyball Kevin Costner stars throwback movie embattled Cleveland Browns GM makes flurry trades get player wants NFL draft The NFL trappings make nice backdrop huge cast sharply written characters well-played famous unknown actors, even GM’s personal life noticeably weaker rest movie The film much better depicting behind-the-scenes dealings, though Costner misses desperation man knows dream job line, underlying coolness helps character keeps head amid pressure His struggle get best losing situation makes movie’s end exhilarating Also Jennifer Garner, Denis Leary, Chadwick Boseman, Josh Pence, Frank Langella, Griffin Newman, Brad Henke, W Earl Brown, Arian Foster, Terry Crews, Tom Welling, Sam Elliott, Sean Combs, Rosanna Arquette, Ellen Burstyn	3	Captain America,comedy,movie,Denis Leary,Scarlett Johansson,pg-13,Terry Crews,Sarah,Patrick,Friday,Sam,historical,Adam,drama,bad,Spider,director,action,film,Neil,fiction,science,story,well,Emma,Tom,good,Peter,Garfield,late,heart,star,race,Gwen,Jones,Stone,great,Cooper,Director,Belle,cast,secret,Dallas,PG,scene,Barrymore,Emily,writer,trade,Agata,long,girl,Anthony,Chris,Man,piece,SHIELD,Webb,Marc,everybody,Giamatti,cameos,century,success,Novak,terror,wonder,Paul,note,18th,character,uncredited,B.J.,enemy,Wilkinson,big,right,ruling,Stacy,music,guy,quiet,court,Sagay,slave,Electro,Davidtz,Foxx,DeHaan,Felicity,romantic,Misan,key,Scott,Embeth,need,Jamie,Goblin,Parker,couple	3391	West,Seth,Old,Liam,Charlize,Neil,Amanda,Sarah,Giovanni,Wes,Gilbert,Christopher,Ewan,Eddie,Anna,Akim,Paweł,Agata,Agata,Dawid,Jerzy,Adam,Halina,Joanna,Angelina,Elle,Sharlto,Lesley,Imelda,Sam,Brenton,Kenneth,Peter,Andrew,Jamie,Dane,Gwen,Emma,Marc,Peter,Gwen,Garfield,Sally,Colm,Campbell,Embeth,Felicity,B.J.,Paul,Denis,Chris,PG,Gugu,Dido,Tom,Amma,Misan,Jane,Sam,Sarah,Tom,Matthew,Penelope,Emily,Miranda,Adam,Drew,Wendi,Barrymore,Bella,Emma,Alyvia,Braxton,Kyle,Terry,Zak,Kevin,Jessica,Abdoulaye,Dan,Shaquille,Joel,Chris,Scarlett,Anthony,Joe,Nick,Samuel,Robert,SHIELD,Captain,Anthony,Cobie,Sebastian,Emily,Dominic,Toby,Frank,Hayley,Jon,Emjay,Roy,Favreau,John,Bobby,Sofia,Oliver,Amy,Scarlett,Dustin,Robert,Shailene,Veronica,Neil,Woodley,Theo,Miles,Jai,Zoë,Ansel,Ray,Maggie,Mekhi,Christian,Tony,Ashley,Kate,Moneyball,Kevin,Cleveland,NFL,NFL,GM,Costner,Jennifer,Denis,Chadwick,Josh,Frank,Griffin,Brad,W.,Arian,Terry,Tom,Sam,Sean,Rosanna,Ellen	202	Captain America,comedy,movie,Denis Leary,Scarlett Johansson,pg-13,Terry Crews,Sarah,Patrick,Friday,Sam,historical,Adam,drama,bad,Spider,director,action,film,Neil,fiction,science,story,well,Emma,Tom,good,Peter,Garfield,late,heart,star,race,Gwen,Jones,Stone,great,Cooper,Director,Belle,cast,secret,Dallas,PG,scene,Barrymore,Emily,writer,trade,Agata,long,girl,Anthony,Chris,Man,piece,SHIELD,Webb,Marc,everybody,Giamatti,cameos,century,success,Novak,terror,wonder,Paul,note,18th,character,uncredited,B.J.,enemy,Wilkinson,big,right,ruling,Stacy,music,guy,quiet,court,Sagay,slave,Electro,Davidtz,Foxx,DeHaan,Felicity,romantic,Misan,key,Scott,Embeth,need,Jamie,Goblin,Parker,couple,West,Seth,Old,Liam,Charlize,Amanda,Giovanni,Wes,Gilbert,Christopher,Ewan,Eddie,Anna,Akim,Paweł,Dawid,Jerzy,Halina,Joanna,Angelina,Elle,Sharlto,Lesley,Imelda,Brenton,Kenneth,Andrew,Dane,Sally,Colm,Campbell,Denis,Gugu,Dido,Amma,Jane,Matthew,Penelope,Miranda,Drew,Wendi,Bella,Alyvia,Braxton,Kyle,Terry,Zak,Kevin,Jessica,Abdoulaye,Dan,Shaquille,Joel,Scarlett,Joe,Nick,Samuel,Robert,Captain,Cobie,Sebastian,Dominic,Toby,Frank,Hayley,Jon,Emjay,Roy,Favreau,John,Bobby,Sofia,Oliver,Amy,Dustin,Shailene,Veronica,Woodley,Theo,Miles,Jai,Zoë,Ansel,Ray,Maggie,Mekhi,Christian,Tony,Ashley,Kate,Moneyball,Cleveland,NFL,GM,Costner,Jennifer,Chadwick,Josh,Griffin,Brad,W.,Arian,Sean,Rosanna,Ellen	3593	opening: a million way to die in the west (r) seth macfarlan star in his own comedi as a coward farmer who must save his old west town from a killer (liam neeson) also with charliz theron, neil patrick harris, amanda seyfried, sarah silverman, giovanni ribisi, wes studi, gilbert gottfried, christoph lloyd, and ewan mcgregor (open friday) alphavill (nr) histor re-releas of jean-luc godard 1965 science-fict film about an american secret agent (eddi constantine) who sent to outer space to free a citi from it dictat also with anna karina and akim tamiroff (open friday in dallas) ida (pg-13) paweł pawlikowski (mi summer of love) direct this drama about a 1960s polish noviti nun (agata trzebuchowska) who is about to take holi order when she learn a terribl secret about her famili also with agata kulesza, dawid ogrodnik, jerzi trela, adam szyszkowski, halina skoczynska, and joanna kulig (open friday in dallas) malefic (pg) angelina joli star in this version of the sleep beauti stori as the vindict fairi who curs a princess (ell fanning) also with sharlto copley, lesley manville, imelda staunton, juno temple, sam riley, brenton thwaites, and kenneth cranham (open friday) now playing: the amaz spider-man 2 (pg-13) better than the last movie, but everybodi here could have been do someth more worthwhil this overstuf sequel featur peter parker (andrew garfield) tri to deal with one too mani bad guy in electro (a too cartoonish jami foxx) and the green goblin (dane dehaan, veri well cast), but the real heart is his need to keep gwen staci (emma stone) from be hurt by spider-man enemi director marc webb keep aim for wonder and terror in the big action set piec and missing; he hit the right note without understand the music he much better in the quieter scene with peter and gwen, as garfield and stone make a loos and funni coupl this director and these star should be make the next great heart-melt romant comedy, not a spider-man movi mayb the success of this will let that happen also with salli field, colm feore, campbel scott, embeth davidtz, felic jones, b j novak, paul giamatti, and uncredit cameo by deni leari and chris cooper bell (pg) a movi that would need to exist even if it histor subject had never live gugu mbatha-raw play dido elizabeth belle, an illegitim child of mix race who was rais on the english estat of her granduncl (tom wilkinson) in the late 18th centuri and may have influenc some key court rule against the slave trade the drama is stilted, and it often feel like director amma asant and writer misan sagay are check off box with all the racial, class, and gender issu in play here still, they find much reward materi in their heroin singular and often uncomfort social posit at it best, this movi play like a jane austen marriag comedi with race thrown into the mix as a volatil element it make this film uniqu also with sam reid, sarah gadon, tom felton, matthew goode, penelop wilton, emili watson, and miranda richardson blend (pg-13) adam sandler latest comedi actual doesn't suck, which is a step up from his last three live-act movi he play a recent widow father of three girl who buy an unus south african vacation, onli to find that he stuck there with a mother of two boy (drew barrymore) whom he had a bad blind date with the movi is too long and never ventur far beyond the resort hotel, and it realli need more of wendi mclendon-covey as barrymor best friend still, the movi is onli overt offens in spot and has a few decent gag like the one involv parasail also with bella thorne, emma fuhrmann, alyvia alyn lind, braxton beckham, kyle red silverstein, terri crews, zak henri, kevin nealon, jessica lowe, abdoulay ngom, dan patrick, shaquill o'neal, and joel mchale captain america: the winter soldier (pg-13) definit better than captain america first outing chris evan return as the superhero tri to deal with a coup insid shield the movi critiqu of the contemporari surveil state doesn't quit hold together, nor doe the flirtati turn in the charact of black widow (scarlett johansson) make much sens yet director anthoni and joe russo do lot of thing well, includ an assassin attempt on the road against nick furi (samuel l jackson) and the chill cast of robert redford as a shield execut with his own agenda captain america is still more interest as a foil to the other aveng than on his own, but this is a worthi excurs also with anthoni mackie, cobi smulders, sebastian stan, emili vancamp, domin cooper, tobi jones, frank grillo, and hayley atwel chef (r) jon favreau star in a not-so-veil comment on his own filmmak career as a star chef who restart his career with a food truck after be fire from a job at an upscal l a restaur the filmmak take way too long to tell his stori and doesn't do well by the women, but he doe captur the chao and sweat and adrenalin of a high-end restaur kitchen, and the subplot with him final connect with his young son (emjay anthony) is nice done the movi also boast scrumptious food photographi (the dish were creat by roy choi), and favreau obvious has great respect for the care and attent to detail that chef give to their work it how the movi hero find himself again, and possibl the filmmak too also with john leguizamo, bobbi cannavale, sofia vergara, oliv platt, ami sedaris, scarlett johansson, dustin hoffman, and robert downey jr diverg (pg-13) ideal view if you'r a teenag for everyon else, not so much shailen woodley star in this science-fict adventur as a girl make her way through a dystopian futur societi divid into faction this is base on veronica roth best-sel novel, which make a neat littl metaphor about how teenag choos cliqu to sort themselv out too bad neither the book nor the film make more of it director neil burger and his writer make hash out of introduc this futur world and show littl humor or phantasmagor power woodley make alert littl choices, but the whole thing lack rhythm, and the action sequenc aren't near good enough to make up for the flat tone also with theo james, mile teller, jai courtney, zoë kravitz, ansel elgort, ray stevenson, maggi q, mekhi phifer, christian madsen, toni goldwyn, ashley judd, and kate winslet draft day (pg-13) better than moneybal kevin costner star in this throwback movi as an embattl cleveland brown gm who make a flurri of trade to get the player he want dure the nfl draft the nfl trap make a nice backdrop for a huge cast of sharpli written charact who are well-play by both the famous and unknown actors, even if the gm person life is notic weaker than the rest of the movi the film is much better at depict the behind-the-scen dealings, and though costner miss the desper of a man who know his dream job is on the line, his under cool help with a charact who keep his head amid the pressur his struggl to get the best out of a lose situat is what make this movi end so exhilar also with jennif garner, deni leary, chadwick boseman, josh pence, frank langella, griffin newman, brad henke, w earl brown, arian foster, terri crews, tom welling, sam elliott, sean combs, rosanna arquette, and ellen burstyn	19	opening: a million way die west (r) seth macfarlan star comedi coward farmer must save old west town killer (liam neeson) also charliz theron, neil patrick harris, amanda seyfried, sarah silverman, giovanni ribisi, wes studi, gilbert gottfried, christoph lloyd, ewan mcgregor (open friday) alphavill (nr) histor re-releas jean-luc godard 1965 science-fict film american secret agent (eddi constantine) who sent outer space free citi dictat also anna karina akim tamiroff (open friday dallas) ida (pg-13) paweł pawlikowski (mi summer love) direct drama 1960s polish noviti nun (agata trzebuchowska) take holi order learn terribl secret famili also agata kulesza, dawid ogrodnik, jerzi trela, adam szyszkowski, halina skoczynska, joanna kulig (open friday dallas) malefic (pg) angelina joli star version sleep beauti stori vindict fairi curs princess (ell fanning) also sharlto copley, lesley manville, imelda staunton, juno temple, sam riley, brenton thwaites, kenneth cranham (open friday) now playing: the amaz spider-man 2 (pg-13) better last movie, everybodi could someth worthwhil this overstuf sequel featur peter parker (andrew garfield) tri deal one mani bad guy electro (a cartoonish jami foxx) green goblin (dane dehaan, well cast), real heart need keep gwen staci (emma stone) hurt spider-man enemi director marc webb keep aim wonder terror big action set piec missing; hit right note without understand music he much better quieter scene peter gwen, garfield stone make loos funni coupl this director star make next great heart-melt romant comedy, spider-man movi mayb success let happen also salli field, colm feore, campbel scott, embeth davidtz, felic jones, b j novak, paul giamatti, uncredit cameo deni leari chris cooper bell (pg) a movi would need exist even histor subject never live gugu mbatha-raw play dido elizabeth belle, illegitim child mix race rais english estat granduncl (tom wilkinson) late 18th centuri may influenc key court rule slave trade the drama stilted, often feel like director amma asant writer misan sagay check box racial, class, gender issu play still, find much reward materi heroin singular often uncomfort social posit at best, movi play like jane austen marriag comedi race thrown mix volatil element it make film uniqu also sam reid, sarah gadon, tom felton, matthew goode, penelop wilton, emili watson, miranda richardson blend (pg-13) adam sandler latest comedi actual doesn't suck, step last three live-act movi he play recent widow father three girl buy unus south african vacation, find he stuck mother two boy (drew barrymore) bad blind date the movi long never ventur far beyond resort hotel, realli need wendi mclendon-covey barrymor best friend still, movi overt offens spot decent gag like one involv parasail also bella thorne, emma fuhrmann, alyvia alyn lind, braxton beckham, kyle red silverstein, terri crews, zak henri, kevin nealon, jessica lowe, abdoulay ngom, dan patrick, shaquill o'neal, joel mchale captain america: the winter soldier (pg-13) definit better captain america first outing chris evan return superhero tri deal coup insid shield the movi critiqu contemporari surveil state doesn't quit hold together, flirtati turn charact black widow (scarlett johansson) make much sens yet director anthoni joe russo lot thing well, includ assassin attempt road nick furi (samuel l jackson) chill cast robert redford shield execut agenda captain america still interest foil aveng own, worthi excurs also anthoni mackie, cobi smulders, sebastian stan, emili vancamp, domin cooper, tobi jones, frank grillo, hayley atwel chef (r) jon favreau star not-so-veil comment filmmak career star chef restart career food truck fire job upscal l a restaur the filmmak take way long tell stori doesn't well women, captur chao sweat adrenalin high-end restaur kitchen, subplot final connect young son (emjay anthony) nice done the movi also boast scrumptious food photographi (the dish creat roy choi), favreau obvious great respect care attent detail chef give work it movi hero find again, possibl filmmak also john leguizamo, bobbi cannavale, sofia vergara, oliv platt, ami sedaris, scarlett johansson, dustin hoffman, robert downey jr diverg (pg-13) ideal view you'r teenag for everyon else, much shailen woodley star science-fict adventur girl make way dystopian futur societi divid faction this base veronica roth best-sel novel, make neat littl metaphor teenag choos cliqu sort too bad neither book film make director neil burger writer make hash introduc futur world show littl humor phantasmagor power woodley make alert littl choices, whole thing lack rhythm, action sequenc aren't near good enough make flat tone also theo james, mile teller, jai courtney, zoë kravitz, ansel elgort, ray stevenson, maggi q, mekhi phifer, christian madsen, toni goldwyn, ashley judd, kate winslet draft day (pg-13) better moneybal kevin costner star throwback movi embattl cleveland brown gm make flurri trade get player want nfl draft the nfl trap make nice backdrop huge cast sharpli written charact well-play famous unknown actors, even gm person life notic weaker rest movi the film much better depict behind-the-scen dealings, though costner miss desper man know dream job line, under cool help charact keep head amid pressur his struggl get best lose situat make movi end exhilar also jennif garner, deni leary, chadwick boseman, josh pence, frank langella, griffin newman, brad henke, w earl brown, arian foster, terri crews, tom welling, sam elliott, sean combs, rosanna arquette, ellen burstyn	17	opening million way die west seth macfarlan star comedi coward farmer must save old west town killer liam neeson also charliz theron neil patrick harris amanda seyfried sarah silverman giovanni ribisi wes studi gilbert gottfried christoph lloyd ewan mcgregor open friday alphavill histor releas jean luc godard science fict film american secret agent eddi constantine who sent outer space free citi dictat also anna karina akim tamiroff open dallas ida pawe pawlikowski summer love direct drama polish noviti nun agata trzebuchowska take holi order learn terribl secret famili also agata kulesza dawid ogrodnik jerzi trela adam szyszkowski halina skoczynska joanna kulig open dallas malefic angelina joli star version sleep beauti vindict fairi curs princess ell fanning also sharlto copley lesley manville imelda staunton juno temple sam riley brenton thwaites kenneth cranham open friday playing amaz spider man better last movie everybodi could someth worthwhil overstuf sequel featur peter parker andrew garfield tri deal one mani bad guy electro cartoonish jami foxx green goblin dane dehaan well cast real heart need keep gwen staci emma stone hurt spider man enemi director marc webb keep aim wonder terror big action set piec missing hit right note without understand music much better quieter scene peter gwen garfield stone make loos funni coupl director star make next great heart melt romant comedy spider man movi mayb success let happen also salli field colm feore campbel scott embeth davidtz felic jones novak paul giamatti uncredit cameo deni leari chris cooper bell movi would need exist even histor subject never live gugu mbatha raw play dido elizabeth belle illegitim child mix race rais english estat granduncl tom wilkinson late centuri influenc key court rule slave trade drama stilted often feel like director amma asant writer misan sagay check box racial class gender issu play still find much reward materi heroin singular often uncomfort social posit best movi play like jane austen marriag comedi race thrown mix volatil element make film uniqu also sam reid sarah gadon tom felton matthew goode penelop wilton emili watson miranda richardson blend adam sandler latest comedi actual doesn suck step last three live act movi play recent widow father three girl buy unus south african vacation find stuck mother two boy drew barrymore bad blind movi long never ventur far beyond resort hotel realli need wendi mclendon covey barrymor best friend still movi overt offens spot decent gag like one involv parasail also bella thorne emma fuhrmann alyvia alyn lind braxton beckham kyle red silverstein terri crews zak henri kevin nealon jessica lowe abdoulay ngom dan patrick shaquill neal joel mchale captain america winter soldier definit better captain america outing chris evan return superhero tri deal coup insid shield movi critiqu contemporari surveil state doesn quit hold together flirtati turn charact black widow scarlett johansson make much sens yet director anthoni joe russo lot thing well includ assassin attempt road nick furi samuel jackson chill cast robert redford shield execut agenda captain america still interest foil aveng own worthi excurs also anthoni mackie cobi smulders sebastian stan emili vancamp domin cooper tobi jones frank grillo hayley atwel chef jon favreau star not veil comment filmmak career star chef restart career food truck fire job upscal restaur filmmak take way long tell doesn well women captur chao sweat adrenalin high end restaur kitchen subplot final connect young son emjay anthony nice done movi also boast scrumptious food photographi the dish creat roy choi favreau obvious great respect care attent detail chef give work movi hero find again possibl filmmak also john leguizamo bobbi cannavale sofia vergara oliv platt ami sedaris scarlett johansson dustin hoffman robert downey diverg ideal view you teenag everyon else much shailen woodley star science fict adventur girl make way dystopian futur societi divid faction base veronica roth best sel novel make neat littl metaphor teenag choos cliqu sort bad neither book film make director neil burger writer make hash introduc futur world show littl humor phantasmagor power woodley make alert littl choices whole thing lack rhythm action sequenc aren near good enough make flat tone also theo james mile teller jai courtney kravitz ansel elgort ray stevenson maggi mekhi phifer christian madsen toni goldwyn ashley judd kate winslet draft better moneybal kevin costner star throwback movi embattl cleveland brown make flurri trade get player want nfl draft nfl trap make nice backdrop huge cast sharpli written charact well play famous unknown actors even person life notic weaker rest movi film much better depict behind the scen dealings though costner miss desper man know dream job line under cool help charact keep head amid pressur struggl get best lose situat make movi end exhilar also jennif garner deni leary chadwick boseman josh pence frank langella griffin newman brad henke earl brown arian foster terri crews tom welling sam elliott sean combs rosanna arquette ellen burstyn	19	"opening : a million Ways to die in the West ( R ) Seth MacFarlane star in his own comedy as a cowardly farmer who must save his Old West town from a killer ( Liam Neeson ).also with Charlize Theron , Neil Patrick Harris , Amanda Seyfried , Sarah Silverman , Giovanni Ribisi , Wes Studi , Gilbert Gottfried , Christopher Lloyd , and Ewan McGregor.( Opens Friday ) 

 Alphaville ( NR ) historical re - release of Jean - Luc Godard ’s 1965 science - fiction film about an american secret agent ( Eddie Constantine ) who ’s send to outer space to free a city from its dictator.also with Anna Karina and Akim Tamiroff.( Opens Friday in Dallas ) 

 Ida ( PG-13 ) Paweł Pawlikowski ( my summer of Love ) direct this drama about a 1960s polish novitiate nun ( Agata Trzebuchowska ) who be about to take holy order when she learn a terrible secret about her family.also with Agata Kulesza , Dawid Ogrodnik , Jerzy Trela , Adam Szyszkowski , Halina Skoczynska , and Joanna Kulig.( Opens Friday in Dallas ) 

 Maleficent ( PG ) Angelina Jolie star in this version of the Sleeping Beauty story as the vindictive fairy who curse a princess ( Elle Fanning ).also with Sharlto Copley , Lesley Manville , Imelda Staunton , Juno Temple , Sam Riley , Brenton Thwaites , and Kenneth Cranham.( Opens Friday ) 

 now play : 

 the amazing Spider - Man 2 ( PG-13 ) well than the last movie , but everybody here could have be do something more worthwhile.This overstuffed sequel feature Peter Parker ( Andrew Garfield ) try to deal with one too many bad guy in Electro ( a too cartoonish Jamie Foxx ) and the Green Goblin ( Dane DeHaan , very well cast ) , but the real heart be his need to keep Gwen Stacy ( Emma Stone ) from be hurt by Spider - Man ’s enemy.Director Marc Webb keep aim for wonder and terror in the big action set piece and miss ; he hit the right note without understand the music.he ’s much better in the quieter scene with Peter and Gwen , as Garfield and Stone make a loose and funny couple.This director and these star should be make the next great heart - melt romantic comedy , not a Spider - Man movie.maybe the success of this will let that happen.also with Sally Field , Colm Feore , Campbell Scott , Embeth Davidtz , Felicity Jones , B.J.Novak , Paul Giamatti , and uncredited cameo by Denis Leary and Chris Cooper.Belle ( PG ) a movie that would need to exist even if its historical subject have never live.Gugu Mbatha - Raw play Dido Elizabeth Belle , an illegitimate child of mixed race who be raise on the english estate of her granduncle ( Tom Wilkinson ) in the late 18th century and may have influence some key court ruling against the slave trade.the drama be stilte , and it often feel like director Amma Asante and writer Misan Sagay be check off box with all the racial , class , and gender issue in play here.still , they find much rewarding material in their heroine ’s singular and often uncomfortable social position.At its good , this movie play like a Jane Austen marriage comedy with race throw into the mix as a volatile element.it make this film unique.also with Sam Reid , Sarah Gadon , Tom Felton , Matthew Goode , Penelope Wilton , Emily Watson , and Miranda Richardson.Blended ( PG-13 ) Adam Sandler ’s late comedy actually do not suck , which be a step up from his last three live - action movie.he play a recently widow father of three girl who buy an unused south african vacation , only to find that he ’s stick there with a mother of two boy ( Drew Barrymore ) whom he have a bad blind date with.the movie be too long and never venture far beyond the resort hotel , and it really need more of Wendi McLendon - Covey as Barrymore ’s good friend.still , the movie be only overtly offensive in spot and have a few decent gag like the one involve parasaile.also with Bella Thorne , Emma Fuhrmann , Alyvia Alyn Lind , Braxton Beckham , Kyle Red Silverstein , Terry Crews , Zak Henri , Kevin Nealon , Jessica Lowe , Abdoulaye Ngom , Dan Patrick , Shaquille O’Neal , and Joel McHale.Captain America : the Winter soldier ( PG-13 ) definitely better than Captain America ’s first outing.Chris Evans return as the superhero try to deal with a coup inside SHIELD.the movie ’s critique of the contemporary surveillance state do not quite hold together , nor do the flirtatious turn in the character of Black Widow ( Scarlett Johansson ) make much sense.yet director Anthony and Joe Russo do lot of thing well , include an assassination attempt on the road against Nick Fury ( Samuel L.Jackson ) and the chilling casting of Robert Redford as a SHIELD executive with his own agenda.Captain America be still more interesting as a foil to the other Avengers than on his own , but this be a worthy excursion.also with Anthony Mackie , Cobie Smulders , Sebastian Stan , Emily VanCamp , Dominic Cooper , Toby Jones , Frank Grillo , and Hayley Atwell.Chef ( R ) Jon Favreau star in a not - so - veil comment on his own filmmaking career as a star chef who restart his career with a food truck after be fire from a job at an upscale l.a.restaurant.the filmmaker take way too long to tell his story and do not do well by the woman , but he do capture the chaos and sweat and adrenaline of a high - end restaurant kitchen , and the subplot with him finally connect with his young son ( Emjay Anthony ) be nicely do.the movie also boast scrumptious food photography ( the dish be create by Roy Choi ) , and Favreau obviously have great respect for the care and attention to detail that chef give to their work.it ’ how the movie ’s hero find himself again , and possibly the filmmaker too.also with John Leguizamo , Bobby Cannavale , Sofia Vergara , Oliver Platt , Amy Sedaris , Scarlett Johansson , Dustin Hoffman , and Robert Downey Jr.Divergent ( PG-13 ) Ideal view if you be a teenager.For everyone else , not so much.Shailene Woodley star in this science - fiction adventure as a girl make her way through a dystopian future society divide into faction.This be base on Veronica Roth ’s best - sell novel , which make a neat little metaphor about how teenager choose clique to sort themselves out.too bad neither the book nor the film make more of it.Director Neil Burger and his writer make hash out of introduce this future world and show little humor or phantasmagoric power.Woodley make alert little choice , but the whole thing lack rhythm , and the action sequence be not nearly good enough to make up for the flat tone.also with Theo James , Miles Teller , Jai Courtney , Zoë Kravitz , Ansel Elgort , Ray Stevenson , Maggie Q , Mekhi Phifer , Christian Madsen , Tony Goldwyn , Ashley Judd , and Kate Winslet.Draft Day ( PG-13 ) well than Moneyball.Kevin Costner star in this throwback movie as an embattle Cleveland Browns GM who make a flurry of trade to get the player he want during the NFL draft.the NFL trapping make a nice backdrop for a huge cast of sharply write character who be well - play by both the famous and unknown actor , even if the GM ’s personal life be noticeably weak than the rest of the movie.the film be much well at depict the behind - the - scene dealing , and though Costner miss the desperation of a man who know his dream job be on the line , his underlie coolness help with a character who keep his head amid the pressure.his struggle to get the good out of a lose situation be what make this movie ’s end so exhilarating.also with Jennifer Garner , Denis Leary , Chadwick Boseman , Josh Pence , Frank Langella , Griffin Newman , Brad Henke , W.Earl Brown , Arian Foster , Terry Crews , Tom Welling , Sam Elliott , Sean Combs , Rosanna Arquette , and Ellen Burstyn."	353	"opening : a million Ways to die in the West ( R ) Seth MacFarlane star in his own comedy as a cowardly farmer who must save his Old West town from a killer ( Liam Neeson ).also with Charlize Theron , Neil Patrick Harris , Amanda Seyfried , Sarah Silverman , Giovanni Ribisi , Wes Studi , Gilbert Gottfried , Christopher Lloyd , and Ewan McGregor.( Opens Friday ) 

 Alphaville ( NR ) historical re - release of Jean - Luc Godard ’s 1965 science - fiction film about an american secret agent ( Eddie Constantine ) who ’s send to outer space to free a city from its dictator.also with Anna Karina and Akim Tamiroff.( Opens Friday in Dallas ) 

 Ida ( PG-13 ) Paweł Pawlikowski ( my summer of Love ) direct this drama about a 1960s polish novitiate nun ( Agata Trzebuchowska ) who is about to take holy order when she learn a terrible secret about her family.also with Agata Kulesza , Dawid Ogrodnik , Jerzy Trela , Adam Szyszkowski , Halina Skoczynska , and Joanna Kulig.( Opens Friday in Dallas ) 

 Maleficent ( PG ) Angelina Jolie star in this version of the Sleeping Beauty story as the vindictive fairy who curse a princess ( Elle Fanning ).also with Sharlto Copley , Lesley Manville , Imelda Staunton , Juno Temple , Sam Riley , Brenton Thwaites , and Kenneth Cranham.( Opens Friday ) 

 now play : 

 the amazing Spider - Man 2 ( PG-13 ) well than the last movie , but everybody here could have been doing something more worthwhile.This overstuffed sequel feature Peter Parker ( Andrew Garfield ) try to deal with one too many bad guy in Electro ( a too cartoonish Jamie Foxx ) and the Green Goblin ( Dane DeHaan , very well cast ) , but the real heart is his need to keep Gwen Stacy ( Emma Stone ) from being hurt by Spider - Man ’s enemy.Director Marc Webb keep aim for wonder and terror in the big action set piece and miss ; he hit the right note without understand the music.he ’s much better in the quieter scene with Peter and Gwen , as Garfield and Stone make a loose and funny couple.This director and these star should be make the next great heart - melt romantic comedy , not a Spider - Man movie.maybe the success of this will let that happen.also with Sally Field , Colm Feore , Campbell Scott , Embeth Davidtz , Felicity Jones , B.J.Novak , Paul Giamatti , and uncredited cameo by Denis Leary and Chris Cooper.Belle ( PG ) a movie that would need to exist even if its historical subject had never live.Gugu Mbatha - Raw play Dido Elizabeth Belle , an illegitimate child of mixed race who was raise on the english estate of her granduncle ( Tom Wilkinson ) in the late 18th century and may have influence some key court ruling against the slave trade.the drama is stilte , and it often feel like director Amma Asante and writer Misan Sagay are check off box with all the racial , class , and gender issue in play here.still , they find much rewarding material in their heroine ’s singular and often uncomfortable social position.At its good , this movie play like a Jane Austen marriage comedy with race throw into the mix as a volatile element.it make this film unique.also with Sam Reid , Sarah Gadon , Tom Felton , Matthew Goode , Penelope Wilton , Emily Watson , and Miranda Richardson.Blended ( PG-13 ) Adam Sandler ’s late comedy actually does n’t suck , which is a step up from his last three live - action movie.he play a recently widow father of three girl who buy an unused south african vacation , only to find that he ’s stick there with a mother of two boy ( Drew Barrymore ) whom he had a bad blind date with.the movie is too long and never venture far beyond the resort hotel , and it really need more of Wendi McLendon - Covey as Barrymore ’s good friend.still , the movie is only overtly offensive in spot and has a few decent gag like the one involve parasaile.also with Bella Thorne , Emma Fuhrmann , Alyvia Alyn Lind , Braxton Beckham , Kyle Red Silverstein , Terry Crews , Zak Henri , Kevin Nealon , Jessica Lowe , Abdoulaye Ngom , Dan Patrick , Shaquille O’Neal , and Joel McHale.Captain America : the Winter soldier ( PG-13 ) definitely better than Captain America ’s first outing.Chris Evans return as the superhero try to deal with a coup inside SHIELD.the movie ’s critique of the contemporary surveillance state does n’t quite hold together , nor does the flirtatious turn in the character of Black Widow ( Scarlett Johansson ) make much sense.yet director Anthony and Joe Russo do lot of thing well , include an assassination attempt on the road against Nick Fury ( Samuel L.Jackson ) and the chilling casting of Robert Redford as a SHIELD executive with his own agenda.Captain America is still more interesting as a foil to the other Avengers than on his own , but this is a worthy excursion.also with Anthony Mackie , Cobie Smulders , Sebastian Stan , Emily VanCamp , Dominic Cooper , Toby Jones , Frank Grillo , and Hayley Atwell.Chef ( R ) Jon Favreau star in a not - so - veil comment on his own filmmaking career as a star chef who restart his career with a food truck after being fire from a job at an upscale l.a.restaurant.the filmmaker take way too long to tell his story and does n’t do well by the woman , but he does capture the chaos and sweat and adrenaline of a high - end restaurant kitchen , and the subplot with him finally connect with his young son ( Emjay Anthony ) is nicely done.the movie also boast scrumptious food photography ( the dish were create by Roy Choi ) , and Favreau obviously has great respect for the care and attention to detail that chef give to their work.it ’ how the movie ’s hero find himself again , and possibly the filmmaker too.also with John Leguizamo , Bobby Cannavale , Sofia Vergara , Oliver Platt , Amy Sedaris , Scarlett Johansson , Dustin Hoffman , and Robert Downey Jr.Divergent ( PG-13 ) Ideal view if you ’re a teenager.For everyone else , not so much.Shailene Woodley star in this science - fiction adventure as a girl make her way through a dystopian future society divide into faction.This is base on Veronica Roth ’s best - sell novel , which make a neat little metaphor about how teenager choose clique to sort themselves out.too bad neither the book nor the film make more of it.Director Neil Burger and his writer make hash out of introduce this future world and show little humor or phantasmagoric power.Woodley make alert little choice , but the whole thing lack rhythm , and the action sequence are n’t nearly good enough to make up for the flat tone.also with Theo James , Miles Teller , Jai Courtney , Zoë Kravitz , Ansel Elgort , Ray Stevenson , Maggie Q , Mekhi Phifer , Christian Madsen , Tony Goldwyn , Ashley Judd , and Kate Winslet.Draft Day ( PG-13 ) well than Moneyball.Kevin Costner star in this throwback movie as an embattle Cleveland Browns GM who make a flurry of trade to get the player he want during the NFL draft.the NFL trapping make a nice backdrop for a huge cast of sharply write character who are well - play by both the famous and unknown actor , even if the GM ’s personal life is noticeably weak than the rest of the movie.the film is much well at depict the behind - the - scene dealing , and though Costner miss the desperation of a man who know his dream job is on the line , his underlie coolness help with a character who keep his head amid the pressure.his struggle to get the good out of a lose situation is what make this movie ’s end so exhilarating.also with Jennifer Garner , Denis Leary , Chadwick Boseman , Josh Pence , Frank Langella , Griffin Newman , Brad Henke , W.Earl Brown , Arian Foster , Terry Crews , Tom Welling , Sam Elliott , Sean Combs , Rosanna Arquette , and Ellen Burstyn."	356	open million way die the west seth macfarlane star his own comedy cowardly farmer who must save his old west town from killer liam neeson also with charlize theron neil patrick harris amanda seyfrie sarah silverman giovanni ribisi wes studi gilbert gottfrie christopher lloyd and ewan mcgregor open friday alphaville historical release jean luc godard science fiction film about american secret agent eddie constantine who send outer space free city from its dictator also with anna karina and akim tamiroff open dalla ida pawe pawlikowski summer love direct this drama about polish novitiate nun agata trzebuchowska who about take holy order when she learn terrible secret about her family also with agata kulesza dawid ogrodnik jerzy trela adam szyszkowski halina skoczynska and joanna kulig open dalla maleficent angelina jolie star this version the sleep beauty the vindictive fairy who curse princess elle fan also with sharlto copley lesley manville imelda staunton juno temple sam riley brenton thwaite and kenneth cranham open friday playing the amazing spider man better than the last movie but everybody here could have been doing something more worthwhile this overstuffed sequel feature peter parker andrew garfield try deal with one too many bad guy electro too cartoonish jamie foxx and the green goblin dane dehaan very well cast but the real heart his need keep gwen stacy emma stone from being hurt spider man enemy director marc webb keep aim for wonder and terror the big action set piece and miss hit the right note without understand the music much better the quieter scene with peter and gwen garfield and stone make loose and funny couple this director and these star should make the next great heart melt romantic comedy not spider man movie maybe the success this will let that happen also with sally field colm feore campbell scott embeth davidtz felicity jone novak paul giamatti and uncredited cameo denis leary and chris cooper belle movie that would need exist even its historical subject had never live gugu mbatha raw play dido elizabeth belle illegitimate child mixed race who was raise the english estate her granduncle tom wilkinson the late century and have influence some key court ruling against the slave trade the drama stilte and often feel like director amma asante and writer misan sagay are check off box with the racial class and gender issue play here still they find much rewarding material their heroine singular and often uncomfortable social position its good this movie play like jane austen marriage comedy with race throw into the mix volatile element make this film unique also with sam reid sarah gadon tom felton matthew goode penelope wilton emily watson and miranda richardson blend adam sandler late comedy actually does suck which step from his last three live action movie play recently widow father three girl who buy unused south african vacation only find that stick there with mother two boy draw barrymore whom had bad blind with the movie too long and never venture far beyond the resort hotel and really need more wendi mclendon covey barrymore good friend still the movie only overtly offensive spot and has few decent gag like the one involve parasaile also with bella thorne emma fuhrmann alyvia alyn lind braxton beckham kyle red silverstein terry crew zak henri kevin nealon jessica lowe abdoulaye ngom dan patrick shaquille neal and joel mchale captain america the winter soldier definitely well than captain america outing chris evan return the superhero try deal with coup inside shield the movie critique the contemporary surveillance state does quite hold together nor does the flirtatious turn the character black widow scarlett johansson make much sense yet director anthony and joe russo lot thing well include assassination attempt the road against nick fury samuel jackson and the chilling casting robert redford shield executive with his own agenda captain america still more interesting foil the other avenger than his own but this worthy excursion also with anthony mackie cobie smulder sebastian stan emily vancamp dominic cooper toby jone frank grillo and hayley atwell chef jon favreau star not veil comment his own filmmaking career star chef who restart his career with food truck after being fire from job upscale restaurant the filmmaker take way too long tell his and does well the woman but does capture the chaos and sweat and adrenaline high end restaurant kitchen and the subplot with him finally connect with his young son emjay anthony nicely done the movie also boast scrumptious food photography the dish were create roy choi and favreau obviously has great respect for the care and attention detail that chef give their work how the movie hero find himself again and possibly the filmmaker too also with john leguizamo bobby cannavale sofia vergara oliver platt amy sedaris scarlett johansson dustin hoffman and robert downey divergent ideal view you teenager for everyone else not much shailene woodley star this science fiction adventure girl make her way through dystopian future society divide into faction this base veronica roth best sell novel which make neat little metaphor about how teenager choose clique sort themselves out too bad neither the book nor the film make more director neil burger and his writer make hash out introduce this future world and show little humor phantasmagoric power woodley make alert little choice but the whole thing lack rhythm and the action sequence are nearly good enough make for the flat tone also with theo jame mile teller jai courtney kravitz ansel elgort ray stevenson maggie mekhi phifer christian madsen tony goldwyn ashley judd and kate winslet draft better than moneyball kevin costn star this throwback movie embattle cleveland brown who make flurry trade get the player want during the nfl draft the nfl trapping make nice backdrop for huge cast sharply write character who are well play both the famous and unknown actor even the personal life noticeably weak than the rest the movie the film much well depict the behind the scene dealing and though costn miss the desperation man who know his dream job the line his underlie coolness help with character who keep his head amid the pressure his struggle get the good out lose situation what make this movie end exhilarating also with jennifer garner denis leary chadwick boseman josh pence frank langella griffin newman brad henke earl brown arian foster terry crew tom welling sam elliott sean comb rosanna arquette and ellen burstyn	368	1	1	0
320774	Today in Photos (June 25)	http://www.spokesman.com/galleries/2014/jun/25/today-photos-june-25/	The Spokesman Review	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.spokesman.com	2014-06-26 19:01:49	1	2014-06-25 00:00:00	en	photos,2014view,25,world,galleries,today,gallery	"Photo galleries Today in Photos (June 25) June 25, 2014

View a gallery of photos from around the world on Wednesday, June 25, 2014."	Photo galleries Today Photos (June 25) June 25, 2014 View gallery photos around world Wednesday, June 25, 2014	0	photo gallery today,June,View,world,Wednesday,Photos	17	empty	12	photo gallery today,June,View,world,Wednesday,Photos,empty	29	photo galleri today in photo (june 25) june 25, 2014 view a galleri of photo from around the world on wednesday, june 25, 2014	1	photo galleri today photo (june 25) june 25, 2014 view galleri photo around world wednesday, june 25, 2014	1	photo galleri photo june view galleri photo around world wednesday	1	"photo gallery today in Photos ( June 25 ) June 25 , 2014 

 View a gallery of photo from around the world on Wednesday , June 25 , 2014."	157	"photo gallery today in Photos ( June 25 ) June 25 , 2014 

 View a gallery of photo from around the world on Wednesday , June 25 , 2014."	147	photo gallery photo june view gallery photo from around the world wednesday	144	1	1	0
320778	Today in Photos (June 26)	http://www.spokesman.com/galleries/2014/jun/26/today-photos-june-26/	The Spokesman Review	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.spokesman.com	2014-06-26 19:01:50	1	2014-06-26 00:00:00	en	photos,2014view,world,galleries,today,26,gallery	"Photo galleries Today in Photos (June 26) June 26, 2014

View a gallery of photos from around the world on Thursday, June 26, 2014."	Photo galleries Today Photos (June 26) June 26, 2014 View gallery photos around world Thursday, June 26, 2014	0	photo gallery today,June,View,world,Thursday,Photos	15	empty	11	photo gallery today,June,View,world,Thursday,Photos,empty	27	photo galleri today in photo (june 26) june 26, 2014 view a galleri of photo from around the world on thursday, june 26, 2014	1	photo galleri today photo (june 26) june 26, 2014 view galleri photo around world thursday, june 26, 2014	1	photo galleri photo june view galleri photo around world thursday	1	"photo gallery today in Photos ( June 26 ) June 26 , 2014 

 View a gallery of photo from around the world on Thursday , June 26 , 2014."	142	"photo gallery today in Photos ( June 26 ) June 26 , 2014 

 View a gallery of photo from around the world on Thursday , June 26 , 2014."	140	photo gallery photo june view gallery photo from around the world thursday	142	1	1	0
320806	Mark Wahlberg Brings His Family to "Transformers" New York Premiere -- See  ...	http://www.toofab.com/2014/06/26/mark-wahlberg-brings-his-family-to-transformers-new-york-premiere/	TooFab.com	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.toofab.com	2014-06-26 19:02:06	1	2014-06-26 00:00:00	en	thing,family,red,carpet,know,things,kids,premiere,mark,cute,brings,dont,maybe,worry,york,think,wahlberg,transformers	is a doting dad!The 43-year-old actor walked the red carpet with his family at the New York premiere of "on Wednesday.He was joined by his wifeand three of their four kids –, 10,, 8, and, 5.Wahlberg is no stranger to showing off his brood!Mark and his son appeared on the cover of the June/July Fatherhood issue of Esquire magazine, where the multi-talented star opened up about what he’s learned since becoming a dad."I think the most important thing is to always be involved in every aspect of their life. To give them enough trust that they can share things with you," he told the mag. "I don’t want them to be terrified of me, you know? But I don’t want them to think they can do whatever they want and get away with it, either, because they can’t.""The biggest thing for me is, you know, as quickly as I was able to turn it around, to get from there to here, from me having nothing as a kid to me here now, providing everything for my kids, it’s like, I worry that maybe they won’t appreciate things," he added. "I worry that maybe they’ll have a sense of entitlement. You don’t wanna give your kids everything without giving them the tools to be great people."We love Mark's candid comments about fatherhood!Click "Launch Gallery" above to see more kids on the red carpet, and check out the pics below to see more cute celebrity kids.	doting dad!The 43-year-old actor walked red carpet family New York premiere "on Wednesday He joined wifeand three four kids –, 10,, 8, and, 5 Wahlberg stranger showing brood!Mark son appeared cover June/July Fatherhood issue Esquire magazine, multi-talented star opened he’s learned since becoming dad "I think important thing always involved every aspect life To give enough trust share things you," told mag "I don’t want terrified me, know? But I don’t want think whatever want get away it, either, can’t ""The biggest thing is, know, quickly I able turn around, get here, nothing kid now, providing everything kids, it’s like, I worry maybe won’t appreciate things," added "I worry maybe they’ll sense entitlement You don’t wanna give kids everything without giving tools great people "We love Mark's candid comments fatherhood!Click "Launch Gallery" see kids red carpet, check pics see cute celebrity kids	1	July Fatherhood issue,great people."We love Mark,red carpet,New York premiere,kid,talented star,important thing,Esquire magazine,old actor,dad!The 43-year,big thing,cute celebrity kid,thing,June,life,trust,cover,son,multi,aspect,brood!Mark,stranger,dad."I,terrified,candid comment,Launch Gallery,able,wifeand,entitlement,sense,tool,Wednesday,fatherhood!Click,pic,family	62	Esquire,Mark	46	July Fatherhood issue,great people."We love Mark,red carpet,New York premiere,kid,talented star,important thing,Esquire magazine,old actor,dad!The 43-year,big thing,cute celebrity kid,thing,June,life,trust,cover,son,multi,aspect,brood!Mark,stranger,dad."I,terrified,candid comment,Launch Gallery,able,wifeand,entitlement,sense,tool,Wednesday,fatherhood!Click,pic,family,Esquire,Mark	108	is a dote dad!th 43-year-old actor walk the red carpet with his famili at the new york premier of "on wednesday he was join by his wifeand three of their four kid –, 10,, 8, and, 5 wahlberg is no stranger to show off his brood!mark and his son appear on the cover of the june/juli fatherhood issu of esquir magazine, where the multi-tal star open up about what he learn sinc becom a dad "i think the most import thing is to alway be involv in everi aspect of their life to give them enough trust that they can share thing with you," he told the mag "i don't want them to be terrifi of me, you know? but i don't want them to think they can do whatev they want and get away with it, either, becaus they can't ""the biggest thing for me is, you know, as quick as i was abl to turn it around, to get from there to here, from me have noth as a kid to me here now, provid everyth for my kids, it like, i worri that mayb they won't appreci things," he ad "i worri that mayb they'll have a sens of entitl you don't wanna give your kid everyth without give them the tool to be great peopl "we love mark candid comment about fatherhood!click "launch gallery" abov to see more kid on the red carpet, and check out the pic below to see more cute celebr kid	4	dote dad!th 43-year-old actor walk red carpet famili new york premier "on wednesday he join wifeand three four kid –, 10,, 8, and, 5 wahlberg stranger show brood!mark son appear cover june/juli fatherhood issu esquir magazine, multi-tal star open he learn sinc becom dad "i think import thing alway involv everi aspect life to give enough trust share thing you," told mag "i don't want terrifi me, know? but i don't want think whatev want get away it, either, can't ""the biggest thing is, know, quick i abl turn around, get here, noth kid now, provid everyth kids, it like, i worri mayb won't appreci things," ad "i worri mayb they'll sens entitl you don't wanna give kid everyth without give tool great peopl "we love mark candid comment fatherhood!click "launch gallery" see kid red carpet, check pic see cute celebr kid	3	dote dad year old actor walk red carpet famili new york premier wednesday join wifeand three four kid and wahlberg stranger show brood mark son appear cover june juli fatherhood issu esquir magazine multi tal star open learn sinc becom dad think import thing alway involv everi aspect life give enough trust share thing you told mag don want terrifi know don want think whatev want get away either can the biggest thing know quick abl turn around get here noth kid now provid everyth kids like worri mayb won appreci things worri mayb they sens entitl don wanna give kid everyth without give tool great peopl love mark candid comment fatherhood click launch gallery see kid red carpet check pic see cute celebr kid	3	be a doting dad!The 43-year - old actor walk the red carpet with his family at the New York premiere of " on Wednesday.he be join by his wifeand three of their four kid – , 10 , , 8 , and , 5.Wahlberg be no stranger to show off his brood!Mark and his son appear on the cover of the June / July Fatherhood issue of Esquire magazine , where the multi - talented star open up about what he ’s learn since become a dad." i think the most important thing be to always be involve in every aspect of their life.to give them enough trust that they can share thing with you , " he tell the mag." i do not want them to be terrify of me , you know ? but i do not want them to think they can do whatever they want and get away with it , either , because they can not." " the big thing for me be , you know , as quickly as i be able to turn it around , to get from there to here , from me have nothing as a kid to me here now , provide everything for my kid , it ’s like , i worry that maybe they will not appreciate thing , " he add." i worry that maybe they will have a sense of entitlement.you do not wanna give your kid everything without give them the tool to be great people." we love Mark 's candid comment about fatherhood!Click " Launch Gallery " above to see more kid on the red carpet , and check out the pic below to see more cute celebrity kid.	180	is a doting dad!The 43-year - old actor walk the red carpet with his family at the New York premiere of " on Wednesday.he was join by his wifeand three of their four kid – , 10 , , 8 , and , 5.Wahlberg is no stranger to show off his brood!Mark and his son appear on the cover of the June / July Fatherhood issue of Esquire magazine , where the multi - talented star open up about what he ’s learn since become a dad." i think the most important thing is to always be involve in every aspect of their life.to give them enough trust that they can share thing with you , " he tell the mag." i do n’t want them to be terrify of me , you know ? but i do n’t want them to think they can do whatever they want and get away with it , either , because they ca n’t." " the big thing for me is , you know , as quickly as i was able to turn it around , to get from there to here , from me having nothing as a kid to me here now , provide everything for my kid , it ’s like , i worry that maybe they wo n’t appreciate thing , " he add." i worry that maybe they ’ll have a sense of entitlement.you do n’t wanna give your kid everything without give them the tool to be great people." we love Mark 's candid comment about fatherhood!Click " Launch Gallery " above to see more kid on the red carpet , and check out the pic below to see more cute celebrity kid.	181	dot dad the year old actor walk the red carpet with his family the new york premiere wednesday was join his wifeand three their four kid and wahlberg stranger show off his brood mark and his son appear the cover the june july fatherhood issue esquire magazine where the multi talented star open about what learn since become dad think the most important thing always involve every aspect their life give them enough trust that they can share thing with you tell the mag want them terrify you know but want them think they can whatever they want and get away with either because they the big thing for you know quickly was able turn around get from there here from having nothing kid here now provide everything for kid like worry that maybe they appreciate thing add worry that maybe they have sense entitlement you wanna give your kid everything without give them the tool great people love mark candid comment about fatherhood click launch gallery above see more kid the red carpet and check out the pic below see more cute celebrity kid	180	1	1	0
320807	Movie review: 'Transformers: Age of Extinction'	http://www.nydailynews.com/entertainment/movies/movie-review-transformers-age-extinction-article-1.1844370	New York Daily News	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.nydailynews.com	2014-06-26 19:02:06	1		en	shia,age,wahlberg,starred,movie,tucci,spitting,snappily,serpent,welcome,yes,extinction,review,transformers,seen	Yes, the Dinobots, when they show up, have a cool look, though they resemble the alien serpent that chased Iron Man in the conclusion of "The Avengers." And Grammer has fun chewing his lines, while Tucci roles his around in his mouth before spitting them out snappily. Wahlberg, too, is a more welcome hero than Shia LaBeouf, who starred in the previous films yet here is blessedly nowhere to be seen.	Yes, Dinobots, show up, cool look, though resemble alien serpent chased Iron Man conclusion "The Avengers " And Grammer fun chewing lines, Tucci roles around mouth spitting snappily Wahlberg, too, welcome hero Shia LaBeouf, starred previous films yet blessedly nowhere seen	0	previous film,Iron Man,Shia LaBeouf,welcome hero,alien serpent,cool look,Tucci,mouth,line,Wahlberg,fun,grammer,Avengers,conclusion,Dinobots	26	Iron,Tucci,Wahlberg,Shia	19	previous film,Iron Man,Shia LaBeouf,welcome hero,alien serpent,cool look,Tucci,mouth,line,Wahlberg,fun,grammer,Avengers,conclusion,Dinobots,Iron,Shia	45	yes, the dinobots, when they show up, have a cool look, though they resembl the alien serpent that chase iron man in the conclus of "the aveng " and grammer has fun chew his lines, while tucci role his around in his mouth befor spit them out snappili wahlberg, too, is a more welcom hero than shia labeouf, who star in the previous film yet here is bless nowher to be seen	1	yes, dinobots, show up, cool look, though resembl alien serpent chase iron man conclus "the aveng " and grammer fun chew lines, tucci role around mouth spit snappili wahlberg, too, welcom hero shia labeouf, star previous film yet bless nowher seen	1	yes dinobots show cool look though resembl alien serpent chase iron man conclus the aveng grammer fun chew lines tucci role around mouth spit snappili wahlberg too welcom hero shia labeouf star previous film yet bless nowher seen	1	yes , the dinobot , when they show up , have a cool look , though they resemble the alien serpent that chase Iron Man in the conclusion of " the avenger." and Grammer have fun chew his line , while Tucci role his around in his mouth before spit them out snappily.wahlberg , too , be a more welcome hero than Shia LaBeouf , who star in the previous film yet here be blessedly nowhere to be see.	154	yes , the dinobot , when they show up , have a cool look , though they resemble the alien serpent that chase Iron Man in the conclusion of " the avenger." and Grammer has fun chew his line , while Tucci role his around in his mouth before spit them out snappily.wahlberg , too , is a more welcome hero than Shia LaBeouf , who star in the previous film yet here is blessedly nowhere to be see.	155	yes the dinobot when they show have cool look though they resemble the alien serpent that chase iron man the conclusion the avenger and grammer has fun chew his line while tucci role his around his mouth before spit them out snappily wahlberg too more welcome hero than shia labeouf who star the previous film yet here blessedly nowhere see	165	1	1	0
320811	MOVIE REVIEW: Hope for a fresh reboot extinguished by bloat and dullness	http://gazette.com/movie-review-hope-for-a-fresh-reboot-extinguished-by-bloat-and-dullness/article/1522064	Colorado Springs Gazette	e	d_FfIMOdatstldMw_ZD6pp24or4YM	gazette.com	2014-06-26 19:02:08	1		en	bloat,subscriptionfor,rate,reboot,stay,hope,movie,fresh,enjoy,monthlysubscribe,unlimiteddigital,weekbilled,offer,access,dullness,extinguished,review,monthslimited	"Enjoy Unlimited

Digital Access with a subscription

For only $2.99 $1.49 per week

(billed monthly)

Subscribe now and stay at this rate for up to 12 months!

Limited time offer!"	Enjoy Unlimited Digital Access subscription For $2 99 $1 49 per week (billed monthly) Subscribe stay rate 12 months! Limited time offer!	0	limited time offer,Digital Access,week,subscription,month,rate,Unlimited	18	empty	13	limited time offer,Digital Access,week,subscription,month,rate,Unlimited,empty	31	enjoy unlimit digit access with a subscript for onli $2 99 $1 49 per week (bill monthly) subscrib now and stay at this rate for up to 12 months! limit time offer!	1	enjoy unlimit digit access subscript for $2 99 $1 49 per week (bill monthly) subscrib stay rate 12 months! limit time offer!	1	enjoy unlimit digit access subscript per week bill monthly subscrib stay rate months limit offer	1	"enjoy Unlimited 

 Digital Access with a subscription 

 For only $ 2.99 $ 1.49 per week 

 ( bill monthly ) 

 Subscribe now and stay at this rate for up to 12 month ! 

 Limited time offer !"	165	"enjoy Unlimited 

 Digital Access with a subscription 

 For only $ 2.99 $ 1.49 per week 

 ( bill monthly ) 

 Subscribe now and stay at this rate for up to 12 month ! 

 Limited time offer !"	156	enjoy unlimited digital access with subscription for only per week bill monthly subscribe and stay this rate for month limited offer	165	1	1	0
320820	Transformers: Age of Extinction Review	http://dorkshelf.com/2014/06/26/transformers-age-of-extinction-review/	DorkShelf.com	e	d_FfIMOdatstldMw_ZD6pp24or4YM	dorkshelf.com	2014-06-26 19:02:13	1	2014-06-26 00:00:00	en	stars,hellboyday,david,age,premiere,contest,harbour,hellboy,milla,httpstco2rtjpremsb,extinction,review,transformers,jovovich	? CONTEST ALERT ? Attend the Canadian Premiere of HELLBOY – with stars David Harbour and Milla Jovovich in attendance! https://t.co/2RtJprEmSB #contest #contestalert #HellboyDay #Hellboy	? CONTEST ALERT ? Attend Canadian Premiere HELLBOY – stars David Harbour Milla Jovovich attendance! https://t co/2RtJprEmSB #contest #contestalert #HellboyDay #Hellboy	0	? contest alert ?,star David Harbour,Canadian Premiere,Milla Jovovich,HellboyDay,contestalert,attendance,HELLBOY	17	HELLBOY,David,Milla	15	? contest alert ?,star David Harbour,Canadian Premiere,Milla Jovovich,HellboyDay,contestalert,attendance,HELLBOY,David,Milla	32	? contest alert ? attend the canadian premier of hellboy – with star david harbour and milla jovovich in attendance! https://t co/2rtjpremsb #contest #contestalert #hellboyday #hellboy	2	? contest alert ? attend canadian premier hellboy – star david harbour milla jovovich attendance! https://t co/2rtjpremsb #contest #contestalert #hellboyday #hellboy	2	contest alert attend canadian premier hellboy star david harbour milla jovovich attendance https rtjpremsb contest contestalert hellboyday hellboy	1	? contest ALERT ? attend the Canadian Premiere of HELLBOY – with star David Harbour and Milla Jovovich in attendance ! https://t.co/2RtJprEmSB # contest # contestalert # HellboyDay # Hellboy	154	? contest ALERT ? attend the Canadian Premiere of HELLBOY – with star David Harbour and Milla Jovovich in attendance ! https://t.co/2RtJprEmSB # contest # contestalert # HellboyDay # Hellboy	151	contest alert attend the canadian premiere hellboy with star david harbour and milla jovovich attendance https rtjpremsb contest contestalert hellboyday hellboy	149	1	1	0
320829	'Transformers: Age of Extinction' movie review: Average yet exciting epic fare	http://www.indiatvnews.com/entertainment/hollywood/tranformers-age-of-extinction-movie-review--8253.html	indiatvnews.com	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.indiatvnews.com	2014-06-26 19:02:16	1	2014-06-26 18:45:00	en	average,sorry,service,epic,age,exciting,region,inconvenience,movie,tvwe,thanks,restricted,india,visiting,extinction,review,transformers,fare	"Thanks for visiting India TV

We have restricted our service in your region for the time being. Sorry for the inconvenience."	Thanks visiting India TV We restricted service region time Sorry inconvenience	0	India TV,time,sorry,region,inconvenience,service,thank	15	empty	11	India TV,time,sorry,region,inconvenience,service,thank,empty	26	thank for visit india tv we have restrict our servic in your region for the time be sorri for the inconveni	1	thank visit india tv we restrict servic region time sorri inconveni	0	thank visit india restrict servic region sorri inconveni	0	"thank for visit India TV 

 we have restrict our service in your region for the time be.sorry for the inconvenience."	149	"thank for visit India TV 

 we have restrict our service in your region for the time being.sorry for the inconvenience."	150	thank for visit india have restrict our service your region for the being sorry for the inconvenience	148	1	1	0
320859	'Transformers' opens tonight	http://www.aberdeennews.com/entertainment/transformers-opens-tonight/article_4d48ca3c-9f78-5a32-b6bd-255870c7bd53.html	AberdeenNews.com	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.aberdeennews.com	2014-06-26 19:02:27	1		en	owner,tonight,opens,transformers,article	You are the owner of this article.	You owner article	0	article,owner	12	empty	8	article,owner,empty	20	you are the owner of this articl	0	you owner articl	0	owner articl	0	you be the owner of this article.	147	you are the owner of this article.	140	you are the owner this article	144	1	1	0
320871	Mark Wahlberg Drops 'Ted 2' Plot Hints, Says It Will Be 'Crazier Than Ever'	http://screenrant.com/ted-2-plot-mark-wahlberg/	Screen Rant	e	d_FfIMOdatstldMw_ZD6pp24or4YM	screenrant.com	2014-06-26 19:02:31	1	2014-06-25 00:00:00	en	john,trip,plot,ted,mark,kunis,theyre,think,road,transformers,drops,crazier,wahlberg,hints,theaters	"870 Shares Share Tweet Email Copy Link Copied

Starting this week, rapper, actor and action star Mark Wahlberg can be seen in theaters opposite some very intimidating co-stars in his latest movie Transformers: Age of Extinction, but next on his agenda is a reunion with a certain naughty, larger-than-life CGI teddy bear named Ted (Seth MacFarlane). The sequel to the 2012 hit, so far just called Ted 2, will begin filming very soon for a summer 2015 release, albeit with a few noticeable changes from the original.

Mila Kunis, who played John Bennett's girlfriend and eventual wife, is not returning outside of maybe a small cameo. Instead, Amanda Seyfried has joined the cast as his new lady love after appearing in MacFarlane's A Million Ways to Die in the West this summer. The news about Kunis leaving and Seyfriend replacing her took fans by surprise earlier this year, and many have wondered what this could mean for the storyline of the sequel.

Sitting down with IGN for Transformers 4, Wahlberg let a few details slip about the plot of Ted 2. He admits that John has not settled down at all since the last film, saying:

"That wouldn't be any fun. No, no, no, they're crazier than ever."

But if Ted was expecting their bromance to get back on track, he should think again - apparently, he'll have a new rival for John's affections in Seyfriend. Said Wahlberg:

"It's a problem, but Ted has bigger issues, bigger fish to fry."

In a previous interview, Wahlberg had hinted that John and Ted may even take their shenanigans "on the road," so at this point it would appear some kind of road trip is in store for the two buddies. However, what this could mean for John or his relationship with either Kunis or Seyfried's characters as he continues "looking for love and everything else there is to look for" is still unclear.

In order for a sequel to be successful, it usually has to differ from the original enough to stand on its own. That said, if the premise changes too much - or resets it as Ted 2 appears to be doing - then the filmmakers run the risk of alienating the same audience they're trying to bring back to theaters.

So what do you think, Screen Rant readers? Are you excited for a soul-searching road trip movie? Or do you just wish Kunis would return for more fun?

_________________________________________________

Ted 2 opens in U.S. theaters on June 26th, 2015.

Source: IGN

Masters of the Universe: Noah Centineo In Talks To Star As He-Man"	870 Shares Share Tweet Email Copy Link Copied Starting week, rapper, actor action star Mark Wahlberg seen theaters opposite intimidating co-stars latest movie Transformers: Age Extinction, next agenda reunion certain naughty, larger-than-life CGI teddy bear named Ted (Seth MacFarlane) The sequel 2012 hit, far called Ted 2, begin filming soon summer 2015 release, albeit noticeable changes original Mila Kunis, played John Bennett's girlfriend eventual wife, returning outside maybe small cameo Instead, Amanda Seyfried joined cast new lady love appearing MacFarlane's A Million Ways Die West summer The news Kunis leaving Seyfriend replacing took fans surprise earlier year, many wondered could mean storyline sequel Sitting IGN Transformers 4, Wahlberg let details slip plot Ted 2 He admits John settled since last film, saying: "That fun No, no, no, they're crazier ever " But Ted expecting bromance get back track, think - apparently, he'll new rival John's affections Seyfriend Said Wahlberg: "It's problem, Ted bigger issues, bigger fish fry " In previous interview, Wahlberg hinted John Ted may even take shenanigans "on road," point would appear kind road trip store two buddies However, could mean John relationship either Kunis Seyfried's characters continues "looking love everything else look for" still unclear In order sequel successful, usually differ original enough stand That said, premise changes much - resets Ted 2 appears - filmmakers run risk alienating audience they're trying bring back theaters So think, Screen Rant readers? Are excited soul-searching road trip movie? Or wish Kunis would return fun? _________________________________________________ Ted 2 opens U S theaters June 26th, 2015 Source: IGN Masters Universe: Noah Centineo In Talks To Star As He-Man	1	life cgi teddy bear,action star Mark Wahlberg,tweet email copy link,Ted,late movie Transformers,new lady love,sequel,John,Kunis,Amanda Seyfried,small cameo,theater,eventual wife,John Bennett,Seth MacFarlane,intimidating co,Mila Kunis,certain naughty,noticeable change,original,summer,Wahlberg,Seyfriend,previous interview,big fish,IGN,new rival,big issue,MacFarlane,road trip,fun,Seyfried,girlfriend,hit,road trip movie,screen rant reader,release,cast,year,surprise,fan,Ways,news,West,storyline,detail,plot,crazy,bromance,track,affection,problem,reunion,large,agenda,Extinction,shenanigan,point,kind,buddy,store,character,relationship,successful,order,unclear,premise,risk,audience,filmmaker,actor,soul,excited,June 26th,U.S. theater,rapper,Noah Centineo,week,source,Masters,Universe,Talks,share	136	Mark,Extinction,CGI,Ted,Seth,Ted,Mila,John,Amanda,MacFarlane,Kunis,Seyfriend,IGN,Wahlberg,Ted,John,Ted,John,Seyfriend,Said,Ted,Wahlberg,John,Ted,John,Kunis,Seyfried,Ted,Kunis,IGN,Noah	78	life cgi teddy bear,action star Mark Wahlberg,tweet email copy link,Ted,late movie Transformers,new lady love,sequel,John,Kunis,Amanda Seyfried,small cameo,theater,eventual wife,John Bennett,Seth MacFarlane,intimidating co,Mila Kunis,certain naughty,noticeable change,original,summer,Wahlberg,Seyfriend,previous interview,big fish,IGN,new rival,big issue,MacFarlane,road trip,fun,Seyfried,girlfriend,hit,road trip movie,screen rant reader,release,cast,year,surprise,fan,Ways,news,West,storyline,detail,plot,crazy,bromance,track,affection,problem,reunion,large,agenda,Extinction,shenanigan,point,kind,buddy,store,character,relationship,successful,order,unclear,premise,risk,audience,filmmaker,actor,soul,excited,June 26th,U.S. theater,rapper,Noah Centineo,week,source,Masters,Universe,Talks,share,Mark,CGI,Seth,Mila,Amanda,Said,Noah	214	870 share share tweet email copi link copi start this week, rapper, actor and action star mark wahlberg can be seen in theater opposit some veri intimid co-star in his latest movi transformers: age of extinction, but next on his agenda is a reunion with a certain naughty, larger-than-lif cgi teddi bear name ted (seth macfarlane) the sequel to the 2012 hit, so far just call ted 2, will begin film veri soon for a summer 2015 release, albeit with a few notic chang from the origin mila kunis, who play john bennett girlfriend and eventu wife, is not return outsid of mayb a small cameo instead, amanda seyfri has join the cast as his new ladi love after appear in macfarlan a million way to die in the west this summer the news about kuni leav and seyfriend replac her took fan by surpris earlier this year, and mani have wonder what this could mean for the storylin of the sequel sit down with ign for transform 4, wahlberg let a few detail slip about the plot of ted 2 he admit that john has not settl down at all sinc the last film, saying: "that wouldn't be ani fun no, no, no, they'r crazier than ever " but if ted was expect their bromanc to get back on track, he should think again - apparently, he'll have a new rival for john affect in seyfriend said wahlberg: "it a problem, but ted has bigger issues, bigger fish to fri " in a previous interview, wahlberg had hint that john and ted may even take their shenanigan "on the road," so at this point it would appear some kind of road trip is in store for the two buddi however, what this could mean for john or his relationship with either kuni or seyfri charact as he continu "look for love and everyth els there is to look for" is still unclear in order for a sequel to be successful, it usual has to differ from the origin enough to stand on it own that said, if the premis chang too much - or reset it as ted 2 appear to be do - then the filmmak run the risk of alien the same audienc they'r tri to bring back to theater so what do you think, screen rant readers? are you excit for a soul-search road trip movie? or do you just wish kuni would return for more fun? _________________________________________________ ted 2 open in u s theater on june 26th, 2015 source: ign master of the universe: noah centineo in talk to star as he-man	6	870 share share tweet email copi link copi start week, rapper, actor action star mark wahlberg seen theater opposit intimid co-star latest movi transformers: age extinction, next agenda reunion certain naughty, larger-than-lif cgi teddi bear name ted (seth macfarlane) the sequel 2012 hit, far call ted 2, begin film soon summer 2015 release, albeit notic chang origin mila kunis, play john bennett girlfriend eventu wife, return outsid mayb small cameo instead, amanda seyfri join cast new ladi love appear macfarlan a million way die west summer the news kuni leav seyfriend replac took fan surpris earlier year, mani wonder could mean storylin sequel sit ign transform 4, wahlberg let detail slip plot ted 2 he admit john settl sinc last film, saying: "that fun no, no, no, they'r crazier ever " but ted expect bromanc get back track, think - apparently, he'll new rival john affect seyfriend said wahlberg: "it problem, ted bigger issues, bigger fish fri " in previous interview, wahlberg hint john ted may even take shenanigan "on road," point would appear kind road trip store two buddi however, could mean john relationship either kuni seyfri charact continu "look love everyth els look for" still unclear in order sequel successful, usual differ origin enough stand that said, premis chang much - reset ted 2 appear - filmmak run risk alien audienc they'r tri bring back theater so think, screen rant readers? are excit soul-search road trip movie? or wish kuni would return fun? _________________________________________________ ted 2 open u s theater june 26th, 2015 source: ign master universe: noah centineo in talk to star as he-man	5	share share tweet email copi link copi start week rapper actor action star mark wahlberg seen theater opposit intimid star latest movi transformers age extinction next agenda reunion certain naughty larger than lif cgi teddi bear name ted seth macfarlane sequel hit far call ted begin film summer release albeit notic chang origin mila kunis play john bennett girlfriend eventu wife return outsid mayb small cameo instead amanda seyfri join cast new ladi love appear macfarlan million way die west summer news kuni leav seyfriend replac took fan surpris earlier year mani wonder could mean storylin sequel sit ign transform wahlberg let detail slip plot ted admit john settl sinc last film saying that fun they crazier ever ted expect bromanc get back track think apparently new rival john affect seyfriend said wahlberg problem ted bigger issues bigger fish fri previous interview wahlberg hint john ted even take shenanigan road point would appear kind road trip store two buddi however could mean john relationship either kuni seyfri charact continu look love everyth els look for still unclear order sequel successful usual differ origin enough stand said premis chang much reset ted appear filmmak run risk alien audienc they tri bring back theater think screen rant readers excit soul search road trip movie wish kuni would return fun ted open theater source ign master universe noah centineo talk star man	6	"870 share Share Tweet Email copy link copy 

 start this week , rapper , actor and action star Mark Wahlberg can be see in theater opposite some very intimidating co - star in his late movie Transformers : Age of Extinction , but next on his agenda be a reunion with a certain naughty , large - than - life cgi teddy bear name Ted ( Seth MacFarlane ).the sequel to the 2012 hit , so far just call Ted 2 , will begin film very soon for a summer 2015 release , albeit with a few noticeable change from the original.Mila Kunis , who play John Bennett 's girlfriend and eventual wife , be not return outside of maybe a small cameo.instead , Amanda Seyfried have join the cast as his new lady love after appear in MacFarlane 's A Million Ways to die in the West this summer.the news about Kunis leave and Seyfriend replace her take fan by surprise earlier this year , and many have wonder what this could mean for the storyline of the sequel.sit down with IGN for transformer 4 , Wahlberg let a few detail slip about the plot of Ted 2.he admit that John have not settle down at all since the last film , say : 

 " that would not be any fun.no , no , no , they be crazy than ever." 

 but if Ted be expect their bromance to get back on track , he should think again - apparently , he will have a new rival for John 's affection in Seyfriend.say Wahlberg : 

 " it be a problem , but Ted have big issue , big fish to fry." 

 In a previous interview , Wahlberg have hint that John and Ted may even take their shenanigan " on the road , " so at this point it would appear some kind of road trip be in store for the two buddy.however , what this could mean for John or his relationship with either Kunis or Seyfried 's character as he continue " look for love and everything else there be to look for " be still unclear.In order for a sequel to be successful , it usually have to differ from the original enough to stand on its own.that say , if the premise change too much - or reset it as Ted 2 appear to be do - then the filmmaker run the risk of alienate the same audience they be try to bring back to theater.so what do you think , Screen Rant reader ? be you excited for a soul - search road trip movie ? or do you just wish Kunis would return for more fun ? 

 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

 Ted 2 open in u.S.theater on June 26th , 2015.source : IGN 

 Masters of the Universe : noah Centineo In talk to star As he - Man"	206	"870 share Share Tweet Email copy link copy 

 start this week , rapper , actor and action star Mark Wahlberg can be see in theater opposite some very intimidating co - star in his late movie Transformers : Age of Extinction , but next on his agenda is a reunion with a certain naughty , large - than - life cgi teddy bear name Ted ( Seth MacFarlane ).the sequel to the 2012 hit , so far just call Ted 2 , will begin film very soon for a summer 2015 release , albeit with a few noticeable change from the original.Mila Kunis , who play John Bennett 's girlfriend and eventual wife , is not return outside of maybe a small cameo.instead , Amanda Seyfried has join the cast as his new lady love after appear in MacFarlane 's A Million Ways to die in the West this summer.the news about Kunis leave and Seyfriend replace her take fan by surprise earlier this year , and many have wonder what this could mean for the storyline of the sequel.sit down with IGN for transformer 4 , Wahlberg let a few detail slip about the plot of Ted 2.he admit that John has not settle down at all since the last film , say : 

 " that would n't be any fun.no , no , no , they 're crazy than ever." 

 but if Ted was expect their bromance to get back on track , he should think again - apparently , he 'll have a new rival for John 's affection in Seyfriend.say Wahlberg : 

 " it 's a problem , but Ted has big issue , big fish to fry." 

 In a previous interview , Wahlberg had hint that John and Ted may even take their shenanigan " on the road , " so at this point it would appear some kind of road trip is in store for the two buddy.however , what this could mean for John or his relationship with either Kunis or Seyfried 's character as he continue " look for love and everything else there is to look for " is still unclear.In order for a sequel to be successful , it usually has to differ from the original enough to stand on its own.that say , if the premise change too much - or reset it as Ted 2 appear to be doing - then the filmmaker run the risk of alienate the same audience they 're try to bring back to theater.so what do you think , Screen Rant reader ? are you excited for a soul - search road trip movie ? or do you just wish Kunis would return for more fun ? 

 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

 Ted 2 open in u.S.theater on June 26th , 2015.source : IGN 

 Masters of the Universe : noah Centineo In talk to star As he - Man"	205	share share tweet email copy link copy start this week rapper actor and action star mark wahlberg can see theater opposite some very intimidating star his late movie transformer age extinction but next his agenda reunion with certain naughty large than life cgi teddy bear name seth macfarlane the sequel the hit far just call will begin film very for summer release albeit with few noticeable change from the original mila kuni who play john bennett girlfriend and eventual wife not return outside maybe small cameo instead amanda seyfrie has join the cast his new lady love after appear macfarlane million way die the west this summer the news about kuni leaving and seyfriend replace her take fan surprise earlier this year and many have wonder what this could mean for the storyline the sequel sit down with ign for transformer wahlberg let few detail slip about the plot admit that john has not settle down since the last film say that would any fun they crazy than ever but was expect their bromance get back track should think again apparently have new rival for john affection seyfriend say wahlberg problem but has big issue big fish fry previous interview wahlberg had hint that john and even take their shenanigan the road this point would appear some kind road trip store for the two buddy however what this could mean for john his relationship with either kuni seyfrie character continue look for love and everything else there look for still unclear order for sequel successful usually has differ from the original enough stand its own that say the premise change too much reset appear doing then the filmmaker run the risk alienate the same audience they try bring back theater what you think screen rant reader are you excited for soul search road trip movie you just wish kuni would return for more fun open theater source ign master the universe noah centineo talk star man	205	1	1	0
320883	Li Bingbing Has Become a Fashion Star with 'Transformers' Tour!	http://www.justjared.com/2014/06/25/li-bingbing-has-become-a-fashion-star-with-transformers-tour/	Just Jared	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.justjared.com	2014-06-26 19:02:35	1	2014-06-25 00:00:00	en	tour,inside,bingbing,premiere,star,check,ziegfeld,li,york,looks,fashion,transformers	"Li Bingbing looks fantastic while walking the carpet at the premiere of her new movie Transformers: Age of Extinction on Wednesday (June 25) at the Ziegfeld Theater in New York City.

The 41-year-old Chinese actress was joined at the event by co-stars Stanley Tucci (with wife Felicity Blunt) and Kelsey Grammer (with kids Mason, 12, and Jude, 9).

PHOTOS: Check out the latest pics of Li Bingbing

Li has become a true fashion star with her amazing looks throughout the Transformers press tour. Make sure to check out our other posts on her!

Also pictured inside: Crossing Jordan star Jill Hennessy attending the premiere.

FYI: Li is wearing a Giambattista Valli dress.

20+ pictures inside of Li Bingbing and others at the premiere…"	Li Bingbing looks fantastic walking carpet premiere new movie Transformers: Age Extinction Wednesday (June 25) Ziegfeld Theater New York City The 41-year-old Chinese actress joined event co-stars Stanley Tucci (with wife Felicity Blunt) Kelsey Grammer (with kids Mason, 12, Jude, 9) PHOTOS: Check latest pics Li Bingbing Li become true fashion star amazing looks throughout Transformers press tour Make sure check posts her! Also pictured inside: Crossing Jordan star Jill Hennessy attending premiere FYI: Li wearing Giambattista Valli dress 20+ pictures inside Li Bingbing others premiere…	1	Crossing Jordan star Jill Hennessy,Li Bingbing,wife Felicity Blunt,Transformers press tour,true fashion star,star Stanley Tucci,old chinese actress,New York City,new movie Transformers,Giambattista Valli dress,Ziegfeld Theater,Li,premiere,kid Mason,Kelsey grammer,late pic,amazing look,June,Wednesday,Extinction,age,41-year,co,carpet,fantastic,event,Jude,photo,sure,post,FYI,picture	41	Li,Stanley,Felicity,Kelsey,Mason,Jude,Li,Transformers,Jill,FYI,Li,Giambattista,Li	27	Crossing Jordan star Jill Hennessy,Li Bingbing,wife Felicity Blunt,Transformers press tour,true fashion star,star Stanley Tucci,old chinese actress,New York City,new movie Transformers,Giambattista Valli dress,Ziegfeld Theater,Li,premiere,kid Mason,Kelsey grammer,late pic,amazing look,June,Wednesday,Extinction,age,41-year,co,carpet,fantastic,event,Jude,photo,sure,post,FYI,picture,Stanley,Felicity,Kelsey,Mason,Transformers,Jill,Giambattista	68	li bingb look fantast while walk the carpet at the premier of her new movi transformers: age of extinct on wednesday (june 25) at the ziegfeld theater in new york citi the 41-year-old chines actress was join at the event by co-star stanley tucci (with wife felic blunt) and kelsey grammer (with kid mason, 12, and jude, 9) photos: check out the latest pic of li bingb li has becom a true fashion star with her amaz look throughout the transform press tour make sure to check out our other post on her! also pictur inside: cross jordan star jill hennessi attend the premier fyi: li is wear a giambattista valli dress 20+ pictur insid of li bingb and other at the premiere…	2	li bingb look fantast walk carpet premier new movi transformers: age extinct wednesday (june 25) ziegfeld theater new york citi the 41-year-old chines actress join event co-star stanley tucci (with wife felic blunt) kelsey grammer (with kid mason, 12, jude, 9) photos: check latest pic li bingb li becom true fashion star amaz look throughout transform press tour make sure check post her! also pictur inside: cross jordan star jill hennessi attend premier fyi: li wear giambattista valli dress 20+ pictur insid li bingb other premiere…	2	bingb look fantast walk carpet premier new movi transformers age extinct june ziegfeld theater new york citi year old chines actress join event star stanley tucci with wife felic blunt kelsey grammer with kid mason jude photos check latest pic bingb becom true fashion star amaz look throughout transform press tour make sure check post her also pictur inside cross jordan star jill hennessi attend premier fyi wear giambattista valli dress pictur insid bingb other premiere	2	"Li Bingbing look fantastic while walk the carpet at the premiere of her new movie transformer : Age of Extinction on Wednesday ( June 25 ) at the Ziegfeld Theater in New York City.the 41-year - old chinese actress be join at the event by co - star Stanley Tucci ( with wife Felicity Blunt ) and Kelsey Grammer ( with kid Mason , 12 , and Jude , 9 ).photos : check out the late pic of Li Bingbing 

 Li have become a true fashion star with her amazing look throughout the Transformers press tour.make sure to check out our other post on her ! 

 also picture inside : cross Jordan star Jill Hennessy attend the premiere.FYI : Li be wear a Giambattista Valli dress.20 + picture inside of Li Bingbing and other at the premiere …"	175	"Li Bingbing look fantastic while walk the carpet at the premiere of her new movie transformer : Age of Extinction on Wednesday ( June 25 ) at the Ziegfeld Theater in New York City.the 41-year - old chinese actress was join at the event by co - star Stanley Tucci ( with wife Felicity Blunt ) and Kelsey Grammer ( with kid Mason , 12 , and Jude , 9 ).photos : check out the late pic of Li Bingbing 

 Li has become a true fashion star with her amazing look throughout the Transformers press tour.make sure to check out our other post on her ! 

 also picture inside : cross Jordan star Jill Hennessy attend the premiere.FYI : Li is wear a Giambattista Valli dress.20 + picture inside of Li Bingbing and others at the premiere …"	170	bingbe look fantastic while walk the carpet the premiere her new movie transformer age extinction june the ziegfeld theater new york city the year old chinese actress was join the event star stanley tucci with wife felicity blunt and kelsey grammer with kid mason and jude photo check out the late pic bingbing has become true fashion star with her amazing look throughout the transformer press tour make sure check out our other post her also picture inside cross jordan star jill hennessy attend the premiere fyi wear giambattista valli dress picture inside bingbing and others the premiere	166	1	1	0
320894	A Look At What General Motors Did To Make Transformers 4: Age Of Extinction  ...	http://gmauthority.com/blog/2014/06/behind-the-scenes-video-of-transformers-age-of-extinction/	GM Authority \(blog\)	e	d_FfIMOdatstldMw_ZD6pp24or4YM	gmauthority.com	2014-06-26 19:02:39	1			age,look,tiein,possible,xp700,cars,product,whet,tieins,video,motors,preview,youll,general,extinction,transformers	"Smokey and the Bandit was one of the most famous product tie-ins ever, although it initially was incidental. However, for the Transformers series, the product tie-in was deliberate, boosting the Camaro’s image and giving fans a limited-edition Camaro that screams “guess what movie I like?”

With Transformers: Age Of Extinction hitting theaters later this month, General Motors felt a behind-the-scenes preview was in order. Certainly the filmmakers couldn’t have done it without GM’s support, as the automaker gave them carte blanche to go nuts with their facilities, including some cars that aren’t quite ready for exposure to the general public. You’ll also find old show cars like the Corvette XP-700, too, if you look hard enough.

Simply put, more resources equals more opportunities to create a Hollywood blockbuster. But don’t let us make you assume it’ll be great—for now, whet your appetite with this preview and see for yourself starting June 27, 2014."	Smokey Bandit one famous product tie-ins ever, although initially incidental However, Transformers series, product tie-in deliberate, boosting Camaro’s image giving fans limited-edition Camaro screams “guess movie I like?” With Transformers: Age Of Extinction hitting theaters later month, General Motors felt behind-the-scenes preview order Certainly filmmakers couldn’t done without GM’s support, automaker gave carte blanche go nuts facilities, including cars aren’t quite ready exposure general public You’ll also find old show cars like Corvette XP-700, too, look hard enough Simply put, resources equals opportunities create Hollywood blockbuster But don’t let us make assume it’ll great—for now, whet appetite preview see starting June 27, 2014	1	old show car,famous product tie,product tie,Transformers series,scene preview,edition Camaro,General Motors,general public,Corvette XP-700,Hollywood blockbuster,preview,Transformers,facility,nut,carte,exposure,automaker,support,Camaro,ready,filmmaker,order,GM,month,fan,theater,image,movie,Extinction,hard,opportunity,deliberate,resource,incidental,ins,Bandit,great,appetite,June,smokey	107	Bandit,Transformers,General,GM,Corvette	35	old show car,famous product tie,product tie,Transformers series,scene preview,edition Camaro,General Motors,general public,Corvette XP-700,Hollywood blockbuster,preview,Transformers,facility,nut,carte,exposure,automaker,support,Camaro,ready,filmmaker,order,GM,month,fan,theater,image,movie,Extinction,hard,opportunity,deliberate,resource,incidental,ins,Bandit,great,appetite,June,smokey,General,Corvette	142	smokey and the bandit was one of the most famous product tie-in ever, although it initi was incident however, for the transform series, the product tie-in was deliberate, boost the camaro imag and give fan a limited-edit camaro that scream “guess what movi i like?” with transformers: age of extinct hit theater later this month, general motor felt a behind-the-scen preview was in order certain the filmmak couldn't have done it without gm support, as the automak gave them cart blanch to go nut with their facilities, includ some car that aren't quit readi for exposur to the general public you'll also find old show car like the corvett xp-700, too, if you look hard enough simpli put, more resourc equal more opportun to creat a hollywood blockbust but don't let us make you assum it'll be great—for now, whet your appetit with this preview and see for yourself start june 27, 2014	3	smokey bandit one famous product tie-in ever, although initi incident however, transform series, product tie-in deliberate, boost camaro imag give fan limited-edit camaro scream “guess movi i like?” with transformers: age of extinct hit theater later month, general motor felt behind-the-scen preview order certain filmmak couldn't done without gm support, automak gave cart blanch go nut facilities, includ car aren't quit readi exposur general public you'll also find old show car like corvett xp-700, too, look hard enough simpli put, resourc equal opportun creat hollywood blockbust but don't let us make assum it'll great—for now, whet appetit preview see start june 27, 2014	2	smokey bandit one famous product tie ever although initi incident however transform series product tie deliberate boost camaro imag give fan limited edit camaro scream guess movi like transformers age extinct hit theater later month general motor felt behind the scen preview order certain filmmak couldn done without support automak gave cart blanch nut facilities includ car aren quit readi exposur general public you also find old show car like corvett too look hard enough simpli put resourc equal opportun creat hollywood blockbust don let make assum great for now whet appetit preview see start	2	"Smokey and the Bandit be one of the most famous product tie - in ever , although it initially be incidental.however , for the Transformers series , the product tie - in be deliberate , boost the Camaro ’s image and give fan a limited - edition Camaro that scream “ guess what movie i like ? " 

 With Transformers : age Of Extinction hit theater later this month , General Motors feel a behind - the - scene preview be in order.certainly the filmmaker could not have do it without GM ’s support , as the automaker give them carte blanche to go nut with their facility , include some car that be not quite ready for exposure to the general public.you will also find old show car like the Corvette xp-700 , too , if you look hard enough.simply put , more resource equal more opportunity to create a Hollywood blockbuster.but do not let us make you assume it will be great — for now , whet your appetite with this preview and see for yourself start June 27 , 2014."	168	"Smokey and the Bandit was one of the most famous product tie - ins ever , although it initially was incidental.however , for the Transformers series , the product tie - in was deliberate , boost the Camaro ’s image and give fan a limited - edition Camaro that scream “ guess what movie i like ? " 

 With Transformers : age Of Extinction hit theater later this month , General Motors feel a behind - the - scene preview was in order.certainly the filmmaker could n’t have done it without GM ’s support , as the automaker give them carte blanche to go nut with their facility , include some car that are n’t quite ready for exposure to the general public.you ’ll also find old show car like the Corvette xp-700 , too , if you look hard enough.simply put , more resource equal more opportunity to create a Hollywood blockbuster.but do n’t let us make you assume it ’ll be great — for now , whet your appetite with this preview and see for yourself start June 27 , 2014."	170	smokey and the bandit was one the most famous product tie ins ever although initially was incidental however for the transformer series the product tie was deliberate boost the camaro image and give fan limited edition camaro that scream guess what movie like with transformer age extinction hit theater later this month general motor feel behind the scene preview was order certainly the filmmaker could have done without support the automaker give them carte blanche nut with their facility include some car that are quite ready for exposure the general public you also find old show car like the corvette too you look hard enough simply put more resource equal more opportunity create hollywood blockbuster but let make you assume great for now whet your appetite with this preview and see for yourself start	171	1	1	0
320931	New movies for the week of June 26, 2014	http://www.theneworleansadvocate.com/beaucoup/9538446-171/new-movies-for-the-week	The New Orleans Advocate	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.theneworleansadvocate.com	2014-06-26 19:02:50	1		en	owner,movies,week,26,article	You are the owner of this article.	You owner article	0	article,owner	12	empty	9	article,owner,empty	20	you are the owner of this articl	1	you owner articl	0	owner articl	0	you be the owner of this article.	143	you are the owner of this article.	143	you are the owner this article	143	1	1	0
320947	Free Transformers Age of Extinction with $25 Transformers toy purchase	http://blog.al.com/bargain-mom/2014/06/free_transformers_age_of_extin.html	The Birmingham News - al.com \(blog\)	e	d_FfIMOdatstldMw_ZD6pp24or4YM	blog.al.com	2014-06-26 19:02:55	1	2014-06-25 06:07:00	en	age,free,toy,week,movie,details,video,25,tshirt,toys,transformer,extinction,transformers,purchase	"Toys R Us has a deal this week - spend $25 on any Transformer toy, video game or movie purchase and get a free movie ticket to the latest Transformers: Age of Extinction.

Go here to check out the offer. Also don't forget the free KRE-O event this Saturday. I shared the details here.

You an also get a free popcorn at Regal if you buy a T-shirt. Details here."	Toys R Us deal week - spend $25 Transformer toy, video game movie purchase get free movie ticket latest Transformers: Age Extinction Go check offer Also forget free KRE-O event Saturday I shared details You also get free popcorn Regal buy T-shirt Details	0	free movie ticket,movie purchase,late Transformers,toy R,video game,O event,Transformer toy,free KRE,free popcorn,detail,week,Extinction,offer,Saturday,Regal,age,shirt,deal	28	Transformer,KRE	21	free movie ticket,movie purchase,late Transformers,toy R,video game,O event,Transformer toy,free KRE,free popcorn,detail,week,Extinction,offer,Saturday,Regal,age,shirt,deal,Transformer,KRE	50	toy r us has a deal this week - spend $25 on ani transform toy, video game or movi purchas and get a free movi ticket to the latest transformers: age of extinct go here to check out the offer also don't forget the free kre-o event this saturday i share the detail here you an also get a free popcorn at regal if you buy a t-shirt detail here	1	toy r us deal week - spend $25 transform toy, video game movi purchas get free movi ticket latest transformers: age extinct go check offer also forget free kre-o event saturday i share detail you also get free popcorn regal buy t-shirt detail	1	toy deal week spend transform toy video game movi purchas get free movi ticket latest transformers age extinct check offer also forget free kre event saturday share detail also get free popcorn regal buy shirt detail	2	toy R us have a deal this week - spend $ 25 on any Transformer toy , video game or movie purchase and get a free movie ticket to the late transformer : age of Extinction.go here to check out the offer.also do not forget the free KRE - O event this Saturday.i share the detail here.you an also get a free popcorn at Regal if you buy a t - shirt.detail here.	159	toy R us has a deal this week - spend $ 25 on any Transformer toy , video game or movie purchase and get a free movie ticket to the late transformer : age of Extinction.go here to check out the offer.also do n't forget the free KRE - O event this Saturday.i share the detail here.you an also get a free popcorn at Regal if you buy a t - shirt.detail here.	158	toy has deal this week spend any transformer toy video game movie purchase and get free movie ticket the late transformer age extinction here check out the offer also forget the free kre event this saturday share the detail here you also get free popcorn regal you buy shirt detail here	157	1	1	0
320957	Alabama players got early look at new Transformers movie	http://collegefootballtalk.nbcsports.com/2014/06/24/alabama-players-got-early-look-at-new-transformers-movie/	NBCSports.com	e	d_FfIMOdatstldMw_ZD6pp24or4YM	collegefootballtalk.nbcsports.com	2014-06-26 19:02:59	1	2014-06-24 00:00:00	en	kansas,kus,early,look,possible,investigation,interview,movie,attorney,beatys,alabama,beaty,ncaa,violations,transformers,players	"David Beaty and Kansas AD Jeff Long are currently locked in a game of he-said/he-said, and the prize is the ex-Jayhawk coach’s $3 million buyout. Beaty is suing the school after alleging KU is looking for a “dead hooker” in his proverbial closet, and Kansas conveniently found one in a possible NCAA violation committed by an unnamed Kansas assistant coach under Beaty’s watch, which would allow them to get out of his contract without paying the buyout.

That investigation, started by Kansas, has since spread to the NCAA, and Kansas has maintained that Beaty has not cooperated with them or the NCAA.

On Tuesday, Beaty’s representatives released a statement to SB Nation saying, in part:

KU’s statement that its review was focused on possible NCAA violations committed by me and that I refused to cooperate is verifiably false. From December 21st of last year to February 1st of this year my attorney sent multiple letters and emails to KU’s attorney trying to get my interview scheduled. Those attempts were accompanied by requests for copies of certain documents of mine that remained in KU’s possession and would allow me to properly prepare and accurately address any concerns. … While the NCAA’s investigative process prohibits me from discussing the investigation or my interview in any detail, I am able to communicate that I voluntarily interviewed with the enforcement staff regarding alleged NCAA violations, and I have fully cooperated with the investigation. I will continue to cooperate with the NCAA should they have any follow-up requests for information but otherwise look forward to the prompt resolution of their work.

Had Kansas simply paid Beaty’s buyout and/or did not discover a possible NCAA violation during the exit interview process (depending on who you believe), Beaty would be almost off KU’s books by now. Instead, the school will either get out from under that $3 million cloud without a drop on them, or they’ll have to pay it and attorney fees."	David Beaty Kansas AD Jeff Long currently locked game he-said/he-said, prize ex-Jayhawk coach’s $3 million buyout Beaty suing school alleging KU looking “dead hooker” proverbial closet, Kansas conveniently found one possible NCAA violation committed unnamed Kansas assistant coach Beaty’s watch, would allow get contract without paying buyout That investigation, started Kansas, since spread NCAA, Kansas maintained Beaty cooperated NCAA On Tuesday, Beaty’s representatives released statement SB Nation saying, part: KU’s statement review focused possible NCAA violations committed I refused cooperate verifiably false From December 21st last year February 1st year attorney sent multiple letters emails KU’s attorney trying get interview scheduled Those attempts accompanied requests copies certain documents mine remained KU’s possession would allow properly prepare accurately address concerns … While NCAA’s investigative process prohibits discussing investigation interview detail, I able communicate I voluntarily interviewed enforcement staff regarding alleged NCAA violations, I fully cooperated investigation I continue cooperate NCAA follow-up requests information otherwise look forward prompt resolution work Had Kansas simply paid Beaty’s buyout and/or discover possible NCAA violation exit interview process (depending believe), Beaty would almost KU’s books Instead, school either get $3 million cloud without drop them, they’ll pay attorney fees	1	unnamed Kansas assistant coach,Kansas AD Jeff Long,possible NCAA violation,Beaty ’s watch,Beaty,KU,David Beaty,buyout,proverbial closet,Jayhawk coach,dead hooker,school,investigation,alleged NCAA violation,multiple letter,SB Nation,February 1st,certain document,December 21st,investigative process,attorney,statement,exit interview process,enforcement staff,year,game,request,contract,prize,prompt resolution,representative,review,Tuesday,email,false,copy,attempt,possession,concern,able,detail,information,work,book,drop,cloud,attorney fee	79	David,Jeff,Beaty,KU,NCAA,Beaty,NCAA,Beaty,NCAA,Beaty,SB,NCAA,KU,KU,NCAA,NCAA,NCAA,Beaty,NCAA,Beaty,KU	55	unnamed Kansas assistant coach,Kansas AD Jeff Long,possible NCAA violation,Beaty ’s watch,Beaty,KU,David Beaty,buyout,proverbial closet,Jayhawk coach,dead hooker,school,investigation,alleged NCAA violation,multiple letter,SB Nation,February 1st,certain document,December 21st,investigative process,attorney,statement,exit interview process,enforcement staff,year,game,request,contract,prize,prompt resolution,representative,review,Tuesday,email,false,copy,attempt,possession,concern,able,detail,information,work,book,drop,cloud,attorney fee,David,Jeff,NCAA,SB	134	david beati and kansa ad jeff long are current lock in a game of he-said/he-said, and the prize is the ex-jayhawk coach $3 million buyout beati is su the school after alleg ku is look for a “dead hooker” in his proverbi closet, and kansa conveni found one in a possibl ncaa violat commit by an unnam kansa assist coach under beati watch, which would allow them to get out of his contract without pay the buyout that investigation, start by kansas, has sinc spread to the ncaa, and kansa has maintain that beati has not cooper with them or the ncaa on tuesday, beati repres releas a statement to sb nation saying, in part: ku statement that it review was focus on possibl ncaa violat commit by me and that i refus to cooper is verifi fals from decemb 21st of last year to februari 1st of this year my attorney sent multipl letter and email to ku attorney tri to get my interview schedul those attempt were accompani by request for copi of certain document of mine that remain in ku possess and would allow me to proper prepar and accur address ani concern … while the ncaa investig process prohibit me from discuss the investig or my interview in ani detail, i am abl to communic that i voluntarili interview with the enforc staff regard alleg ncaa violations, and i have fulli cooper with the investig i will continu to cooper with the ncaa should they have ani follow-up request for inform but otherwis look forward to the prompt resolut of their work had kansa simpli paid beati buyout and/or did not discov a possibl ncaa violat dure the exit interview process (depend on who you believe), beati would be almost off ku book by now instead, the school will either get out from under that $3 million cloud without a drop on them, or they'll have to pay it and attorney fee	5	david beati kansa ad jeff long current lock game he-said/he-said, prize ex-jayhawk coach $3 million buyout beati su school alleg ku look “dead hooker” proverbi closet, kansa conveni found one possibl ncaa violat commit unnam kansa assist coach beati watch, would allow get contract without pay buyout that investigation, start kansas, sinc spread ncaa, kansa maintain beati cooper ncaa on tuesday, beati repres releas statement sb nation saying, part: ku statement review focus possibl ncaa violat commit i refus cooper verifi fals from decemb 21st last year februari 1st year attorney sent multipl letter email ku attorney tri get interview schedul those attempt accompani request copi certain document mine remain ku possess would allow proper prepar accur address concern … while ncaa investig process prohibit discuss investig interview detail, i abl communic i voluntarili interview enforc staff regard alleg ncaa violations, i fulli cooper investig i continu cooper ncaa follow-up request inform otherwis look forward prompt resolut work had kansa simpli paid beati buyout and/or discov possibl ncaa violat exit interview process (depend believe), beati would almost ku book instead, school either get $3 million cloud without drop them, they'll pay attorney fee	4	david beati kansa jeff long current lock game said said prize jayhawk coach million buyout beati school alleg look dead hooker proverbi closet kansa conveni found one possibl ncaa violat commit unnam kansa assist coach beati watch would allow get contract without pay buyout investigation start kansas sinc spread ncaa kansa maintain beati cooper ncaa tuesday beati repres releas statement nation saying part statement review focus possibl ncaa violat commit refus cooper verifi fals last attorney sent multipl letter email attorney tri get interview schedul attempt accompani request copi certain document mine remain possess would allow proper prepar accur address concern ncaa investig process prohibit discuss investig interview detail abl communic voluntarili interview enforc staff regard alleg ncaa violations fulli cooper investig continu cooper ncaa follow request inform otherwis look forward prompt resolut work kansa simpli paid beati buyout and discov possibl ncaa violat exit interview process depend believe beati would almost book instead school either get million cloud without drop them they pay attorney fee	4	"David Beaty and Kansas AD Jeff Long be currently lock in a game of he - say / he - say , and the prize be the ex - Jayhawk coach ’s $ 3 million buyout.Beaty be sue the school after allege KU be look for a " dead hooker " in his proverbial closet , and Kansas conveniently find one in a possible NCAA violation commit by an unnamed Kansas assistant coach under Beaty ’s watch , which would allow them to get out of his contract without pay the buyout.that investigation , start by Kansas , have since spread to the NCAA , and Kansas have maintain that Beaty have not cooperate with them or the NCAA.On Tuesday , Beaty ’s representative release a statement to SB Nation say , in part : 

 KU ’s statement that its review be focus on possible NCAA violation commit by me and that i refuse to cooperate be verifiably false.From December 21st of last year to February 1st of this year my attorney send multiple letter and email to KU ’s attorney try to get my interview schedule.Those attempt be accompany by request for copy of certain document of mine that remain in KU ’s possession and would allow me to properly prepare and accurately address any concern.… While the NCAA ’s investigative process prohibit me from discuss the investigation or my interview in any detail , i be able to communicate that i voluntarily interview with the enforcement staff regard allege NCAA violation , and i have fully cooperate with the investigation.i will continue to cooperate with the NCAA should they have any follow - up request for information but otherwise look forward to the prompt resolution of their work.have Kansas simply pay Beaty ’s buyout and/or do not discover a possible NCAA violation during the exit interview process ( depend on who you believe ) , Beaty would be almost off KU ’s book by now.instead , the school will either get out from under that $ 3 million cloud without a drop on them , or they will have to pay it and attorney fee."	179	"David Beaty and Kansas AD Jeff Long are currently lock in a game of he - say / he - say , and the prize is the ex - Jayhawk coach ’s $ 3 million buyout.Beaty is sue the school after allege KU is look for a " dead hooker " in his proverbial closet , and Kansas conveniently find one in a possible NCAA violation commit by an unnamed Kansas assistant coach under Beaty ’s watch , which would allow them to get out of his contract without pay the buyout.that investigation , start by Kansas , has since spread to the NCAA , and Kansas has maintain that Beaty has not cooperate with them or the NCAA.On Tuesday , Beaty ’s representative release a statement to SB Nation say , in part : 

 KU ’s statement that its review was focus on possible NCAA violation commit by me and that i refuse to cooperate is verifiably false.From December 21st of last year to February 1st of this year my attorney send multiple letter and email to KU ’s attorney try to get my interview schedule.Those attempt were accompany by request for copy of certain document of mine that remain in KU ’s possession and would allow me to properly prepare and accurately address any concern.… While the NCAA ’s investigative process prohibit me from discuss the investigation or my interview in any detail , i am able to communicate that i voluntarily interview with the enforcement staff regard allege NCAA violation , and i have fully cooperate with the investigation.i will continue to cooperate with the NCAA should they have any follow - up request for information but otherwise look forward to the prompt resolution of their work.had Kansas simply pay Beaty ’s buyout and/or did not discover a possible NCAA violation during the exit interview process ( depend on who you believe ) , Beaty would be almost off KU ’s book by now.instead , the school will either get out from under that $ 3 million cloud without a drop on them , or they ’ll have to pay it and attorney fee."	179	david beaty and kansa jeff long are currently lock game say say and the prize the jayhawk coach million buyout beaty sue the school after allege look for dead hooker his proverbial closet and kansa conveniently find one possible ncaa violation commit unnamed kansas assistant coach under beaty watch which would allow them get out his contract without pay the buyout that investigation start kansa has since spread the ncaa and kansa has maintain that beaty has not cooperate with them the ncaa tuesday beaty representative release statement nation say part statement that its review was focus possible ncaa violation commit and that refuse cooperate verifiably false from last this attorney send multiple letter and email attorney try get interview schedule those attempt were accompany request for copy certain document mine that remain possession and would allow properly prepare and accurately address any concern while the ncaa investigative process prohibit from discuss the investigation interview any detail able communicate that voluntarily interview with the enforcement staff regard alleged ncaa violation and have fully cooperate with the investigation will continue cooperate with the ncaa should they have any follow request for information but otherwise look forward the prompt resolution their work had kansa simply pay beaty buyout and did not discover possible ncaa violation during the exit interview process depend who you believe beaty would almost off book now instead the school will either get out from under that million cloud without drop them they have pay and attorney fee	178	1	1	0
320961	Steve Jablonsky Says Transformers Age of Extinction Soundtrack Coming Soon  ...	http://tformers.com/steve-jablonsky-says-transformers-age-of-extinction-soundtrack-coming-soon-as-possible/23959/news.html	Tformers.com	e	d_FfIMOdatstldMw_ZD6pp24or4YM	tformers.com	2014-06-26 19:03:00	1			steve,age,possible,official,try,soundtrack,coming,really,jablonsky,extinction,transformers,soon,page	"It was recommended to me that I start an official Facebook page (since there are other Steve Jablonsky pages that claim to be official), so here it is. Over there we will keep you up to date on things like the Transformers soundtrack, which just a few of you have asked me about I'm very sorry for the lack of information, but rest assured it is in progress and we will have details for you soon. I would tell you now but I'm not quite sure myself. I do know that the music is done!



Also I recently joined Twitter. I really like to stay on top of the latest social media trends If anyone is interested you'll find me at @jablonsky_steve



Have a great week everyone! If you see Age of Extinction I really hope you enjoy it. We will try to make the soundtrack available as soon as possible. Look on the official page for updates. Thank you for all of the amazing messages! I really appreciate them.



Steve

Transformers Age of Extinction music composer, Steve Jablonsky has announced he is launching a new official page on Facebook along with news that they are working on a soundtrack release for the movie: "If you see Age of Extinction I really hope you enjoy it. We will try to make the soundtrack available as soon as possible." Read on to see the full quote about his new official page and the soundtrack below."	It recommended I start official Facebook page (since Steve Jablonsky pages claim official), Over keep date things like Transformers soundtrack, asked I'm sorry lack information, rest assured progress details soon I would tell I'm quite sure I know music done! Also I recently joined Twitter I really like stay top latest social media trends If anyone interested find @jablonsky_steve Have great week everyone! If see Age Extinction I really hope enjoy We try make soundtrack available soon possible Look official page updates Thank amazing messages! I really appreciate Steve Transformers Age Extinction music composer, Steve Jablonsky announced launching new official page Facebook along news working soundtrack release movie: "If see Age Extinction I really hope enjoy We try make soundtrack available soon possible " Read see full quote new official page soundtrack	1	late social medium trend,Steve Jablonsky page,new official page,official Facebook page,Steve Jablonsky,Extinction music composer,Transformers soundtrack,soundtrack available,soundtrack,great week,official page,amazing message,Transformers Age,Age,possible,soundtrack release,Extinction,detail,information,progress,sure,update,Twitter,@jablonsky_steve,interested,lack,sorry,news,movie,quote,thing	56	Facebook,Steve,Transformers,Twitter,@jablonsky_steve,Steve,Steve	40	late social medium trend,Steve Jablonsky page,new official page,official Facebook page,Steve Jablonsky,Extinction music composer,Transformers soundtrack,soundtrack available,soundtrack,great week,official page,amazing message,Transformers Age,Age,possible,soundtrack release,Extinction,detail,information,progress,sure,update,Twitter,@jablonsky_steve,interested,lack,sorry,news,movie,quote,thing,Facebook,Steve,Transformers	96	it was recommend to me that i start an offici facebook page (sinc there are other steve jablonski page that claim to be official), so here it is over there we will keep you up to date on thing like the transform soundtrack, which just a few of you have ask me about i'm veri sorri for the lack of information, but rest assur it is in progress and we will have detail for you soon i would tell you now but i'm not quit sure myself i do know that the music is done! also i recent join twitter i realli like to stay on top of the latest social media trend if anyon is interest you'll find me at @jablonsky_stev have a great week everyone! if you see age of extinct i realli hope you enjoy it we will tri to make the soundtrack avail as soon as possibl look on the offici page for updat thank you for all of the amaz messages! i realli appreci them steve transform age of extinct music composer, steve jablonski has announc he is launch a new offici page on facebook along with news that they are work on a soundtrack releas for the movie: "if you see age of extinct i realli hope you enjoy it we will tri to make the soundtrack avail as soon as possibl " read on to see the full quot about his new offici page and the soundtrack below	3	it recommend i start offici facebook page (sinc steve jablonski page claim official), over keep date thing like transform soundtrack, ask i'm sorri lack information, rest assur progress detail soon i would tell i'm quit sure i know music done! also i recent join twitter i realli like stay top latest social media trend if anyon interest find @jablonsky_stev have great week everyone! if see age extinct i realli hope enjoy we tri make soundtrack avail soon possibl look offici page updat thank amaz messages! i realli appreci steve transform age extinct music composer, steve jablonski announc launch new offici page facebook along news work soundtrack releas movie: "if see age extinct i realli hope enjoy we tri make soundtrack avail soon possibl " read see full quot new offici page soundtrack	3	recommend start offici facebook page sinc steve jablonski page claim official keep thing like transform soundtrack ask sorri lack information rest assur progress detail soon would tell quit sure know music done also recent join twitter realli like stay top latest social media trend anyon interest find jablonsky stev great week everyone see age extinct realli hope enjoy tri make soundtrack avail possibl look offici page updat thank amaz messages realli appreci steve transform age extinct music composer steve jablonski announc launch new offici page facebook along news work soundtrack releas movie see age extinct realli hope enjoy tri make soundtrack avail possibl read see full quot new offici page soundtrack	3	"it be recommend to me that i start an official Facebook page ( since there be other Steve Jablonsky page that claim to be official ) , so here it be.Over there we will keep you up to date on thing like the Transformers soundtrack , which just a few of you have ask me about i be very sorry for the lack of information , but rest assure it be in progress and we will have detail for you soon.i would tell you now but i be not quite sure myself.i do know that the music be do ! 



 also i recently join Twitter.i really like to stay on top of the late social medium trend If anyone be interested you will find me at @jablonsky_steve 



 Have a great week everyone ! If you see Age of Extinction i really hope you enjoy it.we will try to make the soundtrack available as soon as possible.look on the official page for update.thank you for all of the amazing message ! i really appreciate them.Steve 

 Transformers Age of Extinction music composer , Steve Jablonsky have announce he be launch a new official page on Facebook along with news that they be work on a soundtrack release for the movie : " If you see Age of Extinction i really hope you enjoy it.we will try to make the soundtrack available as soon as possible." read on to see the full quote about his new official page and the soundtrack below."	174	"it was recommend to me that i start an official Facebook page ( since there are other Steve Jablonsky page that claim to be official ) , so here it is.Over there we will keep you up to date on thing like the Transformers soundtrack , which just a few of you have ask me about i 'm very sorry for the lack of information , but rest assure it is in progress and we will have detail for you soon.i would tell you now but i 'm not quite sure myself.i do know that the music is done ! 



 also i recently join Twitter.i really like to stay on top of the late social medium trend If anyone is interested you 'll find me at @jablonsky_steve 



 Have a great week everyone ! If you see Age of Extinction i really hope you enjoy it.we will try to make the soundtrack available as soon as possible.look on the official page for update.thank you for all of the amazing message ! i really appreciate them.Steve 

 Transformers Age of Extinction music composer , Steve Jablonsky has announce he is launch a new official page on Facebook along with news that they are work on a soundtrack release for the movie : " If you see Age of Extinction i really hope you enjoy it.we will try to make the soundtrack available as soon as possible." read on to see the full quote about his new official page and the soundtrack below."	175	was recommend that start official facebook page since there are other steve jablonsky page that claim official here over there will keep you thing like the transformer soundtrack which just few you have ask about very sorry for the lack information but rest assure progress and will have detail for you soon would tell you but not quite sure myself know that the music done also recently join twitter really like stay top the late social medium trend anyone interested you find jablonsky steve have great week everyone you see age extinction really hope you enjoy will try make the soundtrack available possible look the official page for update thank you for the amazing message really appreciate them steve transformer age extinction music composer steve jablonsky has announce launch new official page facebook along with news that they are work soundtrack release for the movie you see age extinction really hope you enjoy will try make the soundtrack available possible read see the full quote about his new official page and the soundtrack below	176	1	1	0
320972	Otaku Idol Shokotan Voices Heroine of "Transformers: Age of Extinction"	http://www.crunchyroll.com/anime-news/2014/06/24/otaku-idol-shotakon-to-voice-heroine-of-transformers-age-of-extinction	Crunchyroll News	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.crunchyroll.com	2014-06-26 19:03:03	1	2014-06-24 00:00:00	de	japanese,age,voices,liveaction,otaku,zerudahscott,extinction,role,yogengyo,voice,idol,battle,heroine,shokotan,transformers,z,yeageras	"Though the film doesn't open in Japan until August 8th, otaku TV personality/voice actor/idol singer Shoko "Shokotan" Nakagawa has been introduced as the Japanese voice of Nicola Peltz's Tessa Yeager in the live-action Transformers: Age of Extinction. This character is the daughter of Mark Wahlberg's inventor/single father Cade Yeager.

As well as small and supporting roles such as Yogen-gyo in Dragon Ball Z: Battle of Gods, Shokotan previously substituted for Mandy Moore as Rapunzel in the Japanese dub of Tangled. Last year, she also got her own live-action starring role in Noboru Iguchi's Gothic Lolita Battle Bear.

Ken Watanabe has a role as the English voice of Drift, but Shokotan is so far the only confirmed Japanese cast member.

The movie opens in the US June 27th.

via @ ZERUDAH

-------

Scott Green is editor and reporter for anime and manga at geek entertainment site Ain't It Cool News. Follow him on Twitter at @aicnanime."	Though film open Japan August 8th, otaku TV personality/voice actor/idol singer Shoko "Shokotan" Nakagawa introduced Japanese voice Nicola Peltz's Tessa Yeager live-action Transformers: Age Extinction This character daughter Mark Wahlberg's inventor/single father Cade Yeager As well small supporting roles Yogen-gyo Dragon Ball Z: Battle Gods, Shokotan previously substituted Mandy Moore Rapunzel Japanese dub Tangled Last year, also got live-action starring role Noboru Iguchi's Gothic Lolita Battle Bear Ken Watanabe role English voice Drift, Shokotan far confirmed Japanese cast member The movie opens US June 27th via @ ZERUDAH ------- Scott Green editor reporter anime manga geek entertainment site Ain't It Cool News Follow Twitter @aicnanime	1	Gothic Lolita Battle Bear,single father Cade Yeager,idol singer Shoko,otaku tv personality,Dragon Ball Z,japanese cast member,action Transformers,Shokotan,Tessa Yeager,Mark Wahlberg,Nicola Peltz,voice actor,August 8th,japanese voice,japanese dub,Mandy Moore,live,Noboru Iguchi,role,Ken Watanabe,english voice,geek entertainment site,action,June 27th,Scott Green,gyo,Nakagawa,daughter,Gods,Yogen,character,inventor,battle,Extinction,Rapunzel,year,Tangled,small,Cool News,Drift,Japan,movie,reporter,ZERUDAH,manga,editor,Twitter,@aicnanime,film	100	Shokotan,Nakagawa,Nicola,Tessa,Mark,Cade,Yogen,Shokotan,Mandy,Rapunzel,Gothic,Ken,Drift,Shokotan,Scott,Ai	33	Gothic Lolita Battle Bear,single father Cade Yeager,idol singer Shoko,otaku tv personality,Dragon Ball Z,japanese cast member,action Transformers,Shokotan,Tessa Yeager,Mark Wahlberg,Nicola Peltz,voice actor,August 8th,japanese voice,japanese dub,Mandy Moore,live,Noboru Iguchi,role,Ken Watanabe,english voice,geek entertainment site,action,June 27th,Scott Green,gyo,Nakagawa,daughter,Gods,Yogen,character,inventor,battle,Extinction,Rapunzel,year,Tangled,small,Cool News,Drift,Japan,movie,reporter,ZERUDAH,manga,editor,Twitter,@aicnanime,film,Nicola,Tessa,Mark,Cade,Mandy,Gothic,Ken,Scott,Ai	133	though the film doesn't open in japan until august 8th, otaku tv personality/voic actor/idol singer shoko "shokotan" nakagawa has been introduc as the japanes voic of nicola peltz tessa yeager in the live-act transformers: age of extinct this charact is the daughter of mark wahlberg inventor/singl father cade yeager as well as small and support role such as yogen-gyo in dragon ball z: battl of gods, shokotan previous substitut for mandi moor as rapunzel in the japanes dub of tangl last year, she also got her own live-act star role in noboru iguchi gothic lolita battl bear ken watanab has a role as the english voic of drift, but shokotan is so far the onli confirm japanes cast member the movi open in the us june 27th via @ zerudah ------- scott green is editor and report for anim and manga at geek entertain site ain't it cool news follow him on twitter at @aicnanim	3	though film open japan august 8th, otaku tv personality/voic actor/idol singer shoko "shokotan" nakagawa introduc japanes voic nicola peltz tessa yeager live-act transformers: age extinct this charact daughter mark wahlberg inventor/singl father cade yeager as well small support role yogen-gyo dragon ball z: battl gods, shokotan previous substitut mandi moor rapunzel japanes dub tangl last year, also got live-act star role noboru iguchi gothic lolita battl bear ken watanab role english voic drift, shokotan far confirm japanes cast member the movi open us june 27th via @ zerudah ------- scott green editor report anim manga geek entertain site ain't it cool news follow twitter @aicnanim	2	though film open japan otaku personality voic actor idol singer shoko shokotan nakagawa introduc japanes voic nicola peltz tessa yeager live act transformers age extinct charact daughter mark wahlberg inventor singl father cade yeager well small support role yogen gyo dragon ball battl gods shokotan previous substitut mandi moor rapunzel japanes dub tangl last year also got live act star role noboru iguchi gothic lolita battl bear ken watanab role english voic drift shokotan far confirm japanes cast member movi open via zerudah scott green editor report anim manga geek entertain site ain cool news follow twitter aicnanim	2	"Though the film do not open in Japan until August 8th , otaku tv personality / voice actor / idol singer Shoko " Shokotan " Nakagawa have be introduce as the japanese voice of Nicola Peltz 's Tessa Yeager in the live - action transformer : age of Extinction.This character be the daughter of Mark Wahlberg 's inventor / single father Cade Yeager.as well as small and support role such as Yogen - gyo in Dragon Ball Z : battle of Gods , Shokotan previously substitute for Mandy Moore as Rapunzel in the japanese dub of Tangled.last year , she also get her own live - action star role in Noboru Iguchi 's Gothic Lolita Battle Bear.Ken Watanabe have a role as the english voice of Drift , but Shokotan be so far the only confirm japanese cast member.the movie open in the US June 27th.via @ ZERUDAH 

 ------- 

 Scott Green be editor and reporter for anime and manga at geek entertainment site be not it Cool News.follow him on Twitter at @aicnanime."	197	"Though the film does n't open in Japan until August 8th , otaku tv personality / voice actor / idol singer Shoko " Shokotan " Nakagawa has been introduce as the japanese voice of Nicola Peltz 's Tessa Yeager in the live - action transformer : age of Extinction.This character is the daughter of Mark Wahlberg 's inventor / single father Cade Yeager.as well as small and support role such as Yogen - gyo in Dragon Ball Z : battle of Gods , Shokotan previously substitute for Mandy Moore as Rapunzel in the japanese dub of Tangled.last year , she also get her own live - action star role in Noboru Iguchi 's Gothic Lolita Battle Bear.Ken Watanabe has a role as the english voice of Drift , but Shokotan is so far the only confirm japanese cast member.the movie open in the US June 27th.via @ ZERUDAH 

 ------- 

 Scott Green is editor and reporter for anime and manga at geek entertainment site ai n't it Cool News.follow him on Twitter at @aicnanime."	169	though the film does open japan until otaku personality voice actor idol singer shoko shokotan nakagawa has been introduce the japanese voice nicola peltz tessa yeager the live action transformer age extinction this character the daughter mark wahlberg inventor single father cade yeager well small and support role such yogen gyo dragon ball battle god shokotan previously substitute for mandy moore rapunzel the japanese dub tangle last year she also get her own live action star role noboru iguchi gothic lolita battle bear ken watanabe has role the english voice drift but shokotan far the only confirm japanese cast member the movie open the via zerudah scott green editor and reporter for anime and manga geek entertainment site cool news follow him twitter aicnanime	170	1	1	0
320974	GM Design VP to Make Cameo Appearance in Transformers 4 [Video]	http://www.autoevolution.com/news/gm-design-vp-to-make-cameo-appearance-in-transformers-4-82917.html	autoevolution	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.autoevolution.com	2014-06-26 19:03:04	1	2014-06-24 11:46:00	en	vp,appearance,cameo,design,scene,movie,upcoming,vehicles,office,gm,welburn,spent,transformers	The automaker’s VP of design has filmed a speaking part for the movie that is set to hit Stateside theaters three days from now on, on June 27th. According to Detroit News , a clip from the upcoming Transformers movie was shown to the media recently, depicting Mr. Welburn as an angry man that tells Mark Wahlberg “My office in 15 minutes. I think you know where that is.”Due to the fact that Bumblebee is a robotic hero version of the Chevrolet Camaro and Transformers 4 is chuck-full of vehicles built by General Motors (Corvette Stingray, Sonic and Trax are four-wheel co-stars in the upcoming Hollywood flick), it was somewhat expectable that a bigwig from GM would get a small role in the heavily anticipated movie. Too bad CEO Mary Barra wasn’t available as well, but she’s got her hands full with over 20 million vehicles suffering from various faults, including 2.9 million fitted with sub-standard ignitions.General Motors’ Ed Welburn said he spent a day filming the scene in the automaker’s Design Dome. According to the VP of design, the scene made the cut and it should be included in the movie. A numerous filming crew spent a couple of weeks in 2013 at the GM Tech Center, which was converted into an executive office for the Central Intelligence Agency. “All my car stuff was gone. Every book, every paper was all CIA documents.” Welburn explained.Despite the slightly aggresive product placement, we're keeping our fingers crossed Bumblebee will make it to the end of the movie without being recalled for ignition switch replacement. By the way, did you know that T4 also features a menacing Lamborghini Aventador portraying Lockdown, a Decepticon bounty hunter?	The automaker’s VP design filmed speaking part movie set hit Stateside theaters three days on, June 27th According Detroit News , clip upcoming Transformers movie shown media recently, depicting Mr Welburn angry man tells Mark Wahlberg “My office 15 minutes I think know ”Due fact Bumblebee robotic hero version Chevrolet Camaro Transformers 4 chuck-full vehicles built General Motors (Corvette Stingray, Sonic Trax four-wheel co-stars upcoming Hollywood flick), somewhat expectable bigwig GM would get small role heavily anticipated movie Too bad CEO Mary Barra wasn’t available well, she’s got hands full 20 million vehicles suffering various faults, including 2 9 million fitted sub-standard ignitions General Motors’ Ed Welburn said spent day filming scene automaker’s Design Dome According VP design, scene made cut included movie A numerous filming crew spent couple weeks 2013 GM Tech Center, converted executive office Central Intelligence Agency “All car stuff gone Every book, every paper CIA documents ” Welburn explained Despite slightly aggresive product placement, we're keeping fingers crossed Bumblebee make end movie without recalled ignition switch replacement By way, know T4 also features menacing Lamborghini Aventador portraying Lockdown, Decepticon bounty hunter?	1	automaker ’s Design Dome,bad CEO Mary Barra,upcoming Hollywood flick,robotic hero version,upcoming Transformers movie,General Motors,movie,Central Intelligence Agency,GM Tech Center,numerous filming crew,design,VP,Corvette Stingray,wheel co,Mark Wahlberg,angry man,aggresive product placement,Detroit News,small role,Chevrolet Camaro,Mr. Welburn,day,June 27th,Stateside theater,Ed Welburn,standard ignition,ignition switch replacement,Bumblebee,vehicle,Welburn,executive office,office,car stuff,menacing Lamborghini Aventador,CIA document,clip,medium,minute,fact,is.”Due,Trax,chuck,Sonic,scene,star,bigwig,expectable,available,hand,fault,Decepticon bounty hunter,sub,week,couple,paper,book,finger,end,way,T4,Lockdown	80	Detroit,Transformers,Welburn,Mark,Bumblebee,Chevrolet,General,Corvette,GM,Mary,General,Ed,GM,Central,CIA,Welburn,Bumblebee,Lamborghini,Decepticon	51	automaker ’s Design Dome,bad CEO Mary Barra,upcoming Hollywood flick,robotic hero version,upcoming Transformers movie,General Motors,movie,Central Intelligence Agency,GM Tech Center,numerous filming crew,design,VP,Corvette Stingray,wheel co,Mark Wahlberg,angry man,aggresive product placement,Detroit News,small role,Chevrolet Camaro,Mr. Welburn,day,June 27th,Stateside theater,Ed Welburn,standard ignition,ignition switch replacement,Bumblebee,vehicle,Welburn,executive office,office,car stuff,menacing Lamborghini Aventador,CIA document,clip,medium,minute,fact,is.”Due,Trax,chuck,Sonic,scene,star,bigwig,expectable,available,hand,fault,Decepticon bounty hunter,sub,week,couple,paper,book,finger,end,way,T4,Lockdown,Detroit,Transformers,Mark,Chevrolet,General,Corvette,GM,Mary,Ed,Central,CIA,Lamborghini,Decepticon	131	the automak vp of design has film a speak part for the movi that is set to hit statesid theater three day from now on, on june 27th accord to detroit news , a clip from the upcom transform movi was shown to the media recently, depict mr welburn as an angri man that tell mark wahlberg “mi offic in 15 minut i think you know where that is ”due to the fact that bumblebe is a robot hero version of the chevrolet camaro and transform 4 is chuck-ful of vehicl built by general motor (corvett stingray, sonic and trax are four-wheel co-star in the upcom hollywood flick), it was somewhat expect that a bigwig from gm would get a small role in the heavili anticip movi too bad ceo mari barra wasn't avail as well, but she got her hand full with over 20 million vehicl suffer from various faults, includ 2 9 million fit with sub-standard ignit general motor ed welburn said he spent a day film the scene in the automak design dome accord to the vp of design, the scene made the cut and it should be includ in the movi a numer film crew spent a coupl of week in 2013 at the gm tech center, which was convert into an execut offic for the central intellig agenc “all my car stuff was gone everi book, everi paper was all cia document ” welburn explain despit the slight aggres product placement, we'r keep our finger cross bumblebe will make it to the end of the movi without be recal for ignit switch replac by the way, did you know that t4 also featur a menac lamborghini aventador portray lockdown, a decepticon bounti hunter?	4	the automak vp design film speak part movi set hit statesid theater three day on, june 27th accord detroit news , clip upcom transform movi shown media recently, depict mr welburn angri man tell mark wahlberg “mi offic 15 minut i think know ”due fact bumblebe robot hero version chevrolet camaro transform 4 chuck-ful vehicl built general motor (corvett stingray, sonic trax four-wheel co-star upcom hollywood flick), somewhat expect bigwig gm would get small role heavili anticip movi too bad ceo mari barra wasn't avail well, she got hand full 20 million vehicl suffer various faults, includ 2 9 million fit sub-standard ignit general motor ed welburn said spent day film scene automak design dome accord vp design, scene made cut includ movi a numer film crew spent coupl week 2013 gm tech center, convert execut offic central intellig agenc “all car stuff gone everi book, everi paper cia document ” welburn explain despit slight aggres product placement, we'r keep finger cross bumblebe make end movi without recal ignit switch replac by way, know t4 also featur menac lamborghini aventador portray lockdown, decepticon bounti hunter?	4	automak design film speak part movi set hit statesid theater three accord detroit news clip upcom transform movi shown media recently depict welburn angri man tell mark wahlberg offic minut think know due fact bumblebe robot hero version chevrolet camaro transform chuck ful vehicl built general motor corvett stingray sonic trax four wheel star upcom hollywood flick somewhat expect bigwig would get small role heavili anticip movi bad ceo mari barra wasn avail well she got hand full million vehicl suffer various faults includ million fit sub standard ignit general motor welburn said spent film scene automak design dome accord design scene made cut includ movi numer film crew spent coupl week tech center convert execut offic central intellig agenc all car stuff gone everi book everi paper cia document welburn explain despit slight aggres product placement keep finger cross bumblebe make end movi without recal ignit switch replac way know also featur menac lamborghini aventador portray lockdown decepticon bounti hunter	4	the automaker ’s VP of design have film a speak part for the movie that be set to hit Stateside theater three day from now on , on June 27th.accord to Detroit News , a clip from the upcoming Transformers movie be show to the medium recently , depict Mr.welburn as an angry man that tell Mark Wahlberg “ my office in 15 minute.i think you know where that be." due to the fact that Bumblebee be a robotic hero version of the Chevrolet Camaro and transformer 4 be chuck - full of vehicle build by General Motors ( Corvette Stingray , Sonic and Trax be four - wheel co - star in the upcoming Hollywood flick ) , it be somewhat expectable that a bigwig from GM would get a small role in the heavily anticipate movie.too bad CEO Mary Barra be not available as well , but she ’s get her hand full with over 20 million vehicle suffer from various fault , include 2.9 million fit with sub - standard ignition.General Motors ’ Ed Welburn say he spend a day film the scene in the automaker ’s Design Dome.accord to the VP of design , the scene make the cut and it should be include in the movie.a numerous filming crew spend a couple of week in 2013 at the GM Tech Center , which be convert into an executive office for the Central Intelligence Agency." all my car stuff be go.every book , every paper be all CIA document." welburn explain.Despite the slightly aggresive product placement , we be keep our finger cross Bumblebee will make it to the end of the movie without be recall for ignition switch replacement.By the way , do you know that T4 also feature a menacing Lamborghini Aventador portray Lockdown , a Decepticon bounty hunter ?	192	the automaker ’s VP of design has film a speak part for the movie that is set to hit Stateside theater three day from now on , on June 27th.accord to Detroit News , a clip from the upcoming Transformers movie was show to the medium recently , depict Mr.welburn as an angry man that tell Mark Wahlberg “ my office in 15 minute.i think you know where that is." due to the fact that Bumblebee is a robotic hero version of the Chevrolet Camaro and transformer 4 is chuck - full of vehicle build by General Motors ( Corvette Stingray , Sonic and Trax are four - wheel co - star in the upcoming Hollywood flick ) , it was somewhat expectable that a bigwig from GM would get a small role in the heavily anticipate movie.too bad CEO Mary Barra was n’t available as well , but she ’s get her hand full with over 20 million vehicle suffer from various fault , include 2.9 million fit with sub - standard ignition.General Motors ’ Ed Welburn say he spend a day film the scene in the automaker ’s Design Dome.accord to the VP of design , the scene make the cut and it should be include in the movie.a numerous filming crew spend a couple of week in 2013 at the GM Tech Center , which was convert into an executive office for the Central Intelligence Agency." all my car stuff was go.every book , every paper was all CIA document." welburn explain.Despite the slightly aggresive product placement , we 're keep our finger cross Bumblebee will make it to the end of the movie without being recall for ignition switch replacement.By the way , did you know that T4 also feature a menacing Lamborghini Aventador portray Lockdown , a Decepticon bounty hunter ?	192	the automaker design has film speak part for the movie that set hit stateside theater three from accord detroit news clip from the upcoming transformer movie was show the medium recently depict welburn angry man that tell mark wahlberg office minute think you know where that due the fact that bumblebee robotic hero version the chevrolet camaro and transformer chuck full vehicle build general motor corvette stingray sonic and trax are four wheel star the upcoming hollywood flick was somewhat expectable that bigwig from would get small role the heavily anticipate movie too bad ceo mary barra was available well but she get her hand full with over million vehicle suffer from various fault include million fit with sub standard ignition general motor welburn say spend filming the scene the automaker design dome accord the design the scene make the cut and should include the movie numerous filming crew spend couple week the tech center which was convert into executive office for the central intelligence agency all car stuff was every book every paper was cia document welburn explain despite the slightly aggresive product placement keep our finger cross bumblebee will make the end the movie without being recall for ignition switch replacement the way did you know that also feature menacing lamborghini aventador portray lockdown decepticon bounty hunter	192	1	1	0
320977	'Transformers' counterprogramming: What else to watch in NYC	http://www.amny.com/entertainment/transformers-counterprogramming-what-else-to-watch-in-nyc-1.8542745	amNY	e	d_FfIMOdatstldMw_ZD6pp24or4YM	www.amny.com	2014-06-26 19:03:05	1	2014-06-23 17:20:25	en	counterprogramming,vacation,way,williamsburg,venue,wahlberg,worth,weekendheres,nyc,watch,weekthere,websiteifc,transformers,smaller	"Unless you really love the thought of spending nearly three hours with Mark Wahlberg and enormous robots, you might very well be in search of an alternative to "Transformers: Age of Extinction" this week.

There are lots of strong options.

In addition to all the smaller movies in theaters and continuing series such as BAMcinemaFest, several classics will be screening this weekend.

Here's a breakdown by venue. Showtimes and more info at each website:

IFC Center:

"The Terminator" is smaller and grittier than its heralded sequel, but it's definitely worth the price of admission.

The surrealist masterpiece "Eraserhead," David Lynch's feature filmmaking debut, remains one of his most deeply unsettling movies.

Nitehawk Cinema:

Eat it. Drink it. Do it. Tackle the city, with our help. By clicking Sign up, you agree to our privacy policy.

The Williamsburg hot spot is showing "The Holy Mountain," from the greatest midnight filmmaker, Alejandro Jodorowsky, John Carpenter's superb "The Thing," Alfred Hitchcock's "North by Northwest" and more.

Landmark Sunshine Cinema:

There's no better way to pay tribute to the late Harold Ramis than by once again experiencing the Griswold's original "Vacation," which he directed."	Unless really love thought spending nearly three hours Mark Wahlberg enormous robots, might well search alternative "Transformers: Age Extinction" week There lots strong options In addition smaller movies theaters continuing series BAMcinemaFest, several classics screening weekend Here's breakdown venue Showtimes info website: IFC Center: "The Terminator" smaller grittier heralded sequel, definitely worth price admission The surrealist masterpiece "Eraserhead," David Lynch's feature filmmaking debut, remains one deeply unsettling movies Nitehawk Cinema: Eat Drink Do Tackle city, help By clicking Sign up, agree privacy policy The Williamsburg hot spot showing "The Holy Mountain," greatest midnight filmmaker, Alejandro Jodorowsky, John Carpenter's superb "The Thing," Alfred Hitchcock's "North Northwest" Landmark Sunshine Cinema: There's better way pay tribute late Harold Ramis experiencing Griswold's original "Vacation," directed	1	late Harold Ramis,Landmark Sunshine Cinema,great midnight filmmaker,feature filmmaking debut,Williamsburg hot spot,small movie,enormous robot,Nitehawk Cinema,David Lynch,strong option,heralded sequel,IFC Center,surrealist masterpiece,unsettling movie,Mark Wahlberg,privacy policy,John Carpenter,Holy Mountain,Alejandro Jodorowsky,Alfred Hitchcock,well way,small,website,info,admission,showtime,gritty,Eraserhead,Terminator,price,venue,worth,classic,weekend,breakdown,BAMcinemaFest,series,theater,Extinction,Sign,help,addition,lot,city,age,Transformers,thing,alternative,superb,Northwest,search,hour,tribute,Griswold,original,vacation,thought	161	Mark,BAMcinemaFest,David,Nitehawk,Alejandro,John,Alfred,Harold,Griswold	41	late Harold Ramis,Landmark Sunshine Cinema,great midnight filmmaker,feature filmmaking debut,Williamsburg hot spot,small movie,enormous robot,Nitehawk Cinema,David Lynch,strong option,heralded sequel,IFC Center,surrealist masterpiece,unsettling movie,Mark Wahlberg,privacy policy,John Carpenter,Holy Mountain,Alejandro Jodorowsky,Alfred Hitchcock,well way,small,website,info,admission,showtime,gritty,Eraserhead,Terminator,price,venue,worth,classic,weekend,breakdown,BAMcinemaFest,series,theater,Extinction,Sign,help,addition,lot,city,age,Transformers,thing,alternative,superb,Northwest,search,hour,tribute,Griswold,original,vacation,thought,Mark,David,Nitehawk,Alejandro,John,Alfred,Harold	202	unless you realli love the thought of spend near three hour with mark wahlberg and enorm robots, you might veri well be in search of an altern to "transformers: age of extinction" this week there are lot of strong option in addit to all the smaller movi in theater and continu seri such as bamcinemafest, sever classic will be screen this weekend here a breakdown by venu showtim and more info at each website: ifc center: "the terminator" is smaller and grittier than it herald sequel, but it definit worth the price of admiss the surrealist masterpiec "eraserhead," david lynch featur filmmak debut, remain one of his most deepli unsettl movi nitehawk cinema: eat it drink it do it tackl the city, with our help by click sign up, you agre to our privaci polici the williamsburg hot spot is show "the holi mountain," from the greatest midnight filmmaker, alejandro jodorowsky, john carpent superb "the thing," alfr hitchcock "north by northwest" and more landmark sunshin cinema: there no better way to pay tribut to the late harold rami than by onc again experienc the griswold origin "vacation," which he direct	3	unless realli love thought spend near three hour mark wahlberg enorm robots, might well search altern "transformers: age extinction" week there lot strong option in addit smaller movi theater continu seri bamcinemafest, sever classic screen weekend here breakdown venu showtim info website: ifc center: "the terminator" smaller grittier herald sequel, definit worth price admiss the surrealist masterpiec "eraserhead," david lynch featur filmmak debut, remain one deepli unsettl movi nitehawk cinema: eat drink do tackl city, help by click sign up, agre privaci polici the williamsburg hot spot show "the holi mountain," greatest midnight filmmaker, alejandro jodorowsky, john carpent superb "the thing," alfr hitchcock "north northwest" landmark sunshin cinema: there better way pay tribut late harold rami experienc griswold origin "vacation," direct	3	unless realli love thought spend near three mark wahlberg enorm robots might well search altern transformers age extinction week lot strong option addit smaller movi theater continu seri bamcinemafest sever classic screen weekend here breakdown venu showtim info website ifc center the terminator smaller grittier herald sequel definit worth price admiss surrealist masterpiec eraserhead david lynch featur filmmak debut remain one deepli unsettl movi nitehawk cinema eat drink tackl city help click sign agre privaci polici williamsburg hot spot show the holi mountain greatest midnight filmmaker alejandro jodorowsky john carpent superb the thing alfr hitchcock north northwest landmark sunshin cinema there better way pay tribut late harold rami experienc griswold origin vacation direct	3	"Unless you really love the thought of spend nearly three hour with Mark Wahlberg and enormous robot , you may very well be in search of an alternative to " transformer : age of Extinction " this week.there be lot of strong option.In addition to all the small movie in theater and continue series such as BAMcinemaFest , several classic will be screen this weekend.here be a breakdown by venue.showtime and more info at each website : 

 IFC Center : 

 " the Terminator " be small and gritty than its heralded sequel , but it be definitely worth the price of admission.the surrealist masterpiece " eraserhead , " David Lynch 's feature filmmaking debut , remain one of his most deeply unsettling movie.Nitehawk Cinema : 

 eat it.drink it.Do it.tackle the city , with our help.By click Sign up , you agree to our privacy policy.the Williamsburg hot spot be show " the Holy Mountain , " from the great midnight filmmaker , Alejandro Jodorowsky , John Carpenter 's superb " the thing , " Alfred Hitchcock 's " North by Northwest " and more.Landmark Sunshine Cinema : 

 there be no well way to pay tribute to the late Harold Ramis than by once again experience the Griswold 's original " vacation , " which he direct."	186	"Unless you really love the thought of spend nearly three hour with Mark Wahlberg and enormous robot , you may very well be in search of an alternative to " transformer : age of Extinction " this week.there are lot of strong option.In addition to all the small movie in theater and continue series such as BAMcinemaFest , several classic will be screen this weekend.here 's a breakdown by venue.showtime and more info at each website : 

 IFC Center : 

 " the Terminator " is small and gritty than its heralded sequel , but it 's definitely worth the price of admission.the surrealist masterpiece " eraserhead , " David Lynch 's feature filmmaking debut , remain one of his most deeply unsettling movie.Nitehawk Cinema : 

 eat it.drink it.Do it.tackle the city , with our help.By click Sign up , you agree to our privacy policy.the Williamsburg hot spot is show " the Holy Mountain , " from the great midnight filmmaker , Alejandro Jodorowsky , John Carpenter 's superb " the thing , " Alfred Hitchcock 's " North by Northwest " and more.Landmark Sunshine Cinema : 

 there 's no well way to pay tribute to the late Harold Ramis than by once again experience the Griswold 's original " vacation , " which he direct."	188	unless you really love the thought spend nearly three with mark wahlberg and enormous robot you may very well search alternative transformer age extinction this week there are lot strong option addition the small movie theater and continue series such bamcinemaf several classic will screen this weekend here breakdown venue showtime and more info each website ifc center the terminator small and gritty than its heralded sequel but definitely worth the price admission the surrealist masterpiece eraserhead david lynch feature filmmaking debut remain one his most deeply unsettling movie nitehawk cinema eat drink tackle the city with our help click sign you agree our privacy policy the williamsburg hot spot show the holy mountain from the great midnight filmmaker alejandro jodorowsky john carpenter superb the thing alfred hitchcock north northwest and more landmark sunshine cinema there well way pay tribute the late harold ramis than once again experience the griswold original vacation which direct	188	1	1	0
331140	Top 10 fines imposed on banks by the US	http://www.moneyweb.co.za/moneyweb-international/top-10-fines-imposed-on-banks-by-the-us	Moneyweb.co.za	b	d_IY8r2JZTWLvkMrM33bhyNY2EkzM	www.moneyweb.co.za	2014-06-30 00:30:01	1			paid,pay,imposed,fine,bank,mortgage,banks,fines,agreed,jpmorgan,billion,securities,avoid	"French bank BNP Paribas is expected to pay a record $9 billion fine for years of dealing with US-blacklisted Sudan and Iran, in a case that has strained ties between Paris and Washington. It will be a record US fine of a foreign bank.

Below is a list of the 10 largest fines in US banking history:

– $25 billion: Wells Fargo, JPMorgan Chase, Citigroup, Bank of America, Ally Financial

In February 2012, the banks collectively agreed to pay this amount — $20 billion in various forms of relief for home-loan borrowers and $5 billion in penalties and contributions to a cash fund for unfairly foreclosed homes — to avoid prosecution over abuses.

– $13 billion: JPMorgan Chase

The bank, Wall Street’s former poster child, paid in November 2013 to resolve a series of US and state lawsuits over the sale of toxic mortgage-backed securities.

– $11.6 billion: Bank of America

One of the rare big US banks whose headquarters is not in New York, the North Carolina-based Bank of America also paid the biggest penalty for the subprime mortgage crisis.

In January 2013, BofA paid this fine to settle claims that it sold US government-controlled mortgage finance giant Fannie Mae hundreds of billions of dollars’ worth of dud home loans.

– $9.5 billion: Bank of America

On March 26 this year, the bank, America’s second-largest lender in assets, agreed to pay $9.5 billion to settle litigation by the Federal Housing Finance Agency over mortgage securities sold to Fannie Mae and fellow agency Freddie Mac.

– $8.5 billion: Bank of America

In June 2011 the bank agreed to compensate a group of investors who said they lost money on mortgage-backed securities bought before the financial crisis.

– $2.6 billion: Credit Suisse

In May 2014 the bank pleaded guilty to helping rich Americans lie to avoid paying taxes.

– $1.9 billion: HSBC

The British bank agreed to pay up in December 2012 to avoid prosecution for complicity in money laundering.

– $1.7 billion: JPMorgan Chase

In January the bank agreed to cough up to resolve charges its lax oversight enabled Bernard Madoff to build up the massive Ponzi scheme that bilked investors of billions.

– $1.5 billion: UBS

In December 2012 the Swiss bank paid out to put an end to legal proceedings linked to the alleged fixing of the inter-bank Libor interest rate.

– $1.0 billion: Rabobank

The Dutch bank paid just over $1.0 billion in October 2013 also for proceedings over the alleged Libor rate rigging.

Other cases under way could smash these records.

Bank of America is facing a possibly $12-$17 billion penalty, while Citigroup could be facing as much as $10 billion, both over bad business practices in mortgages which were the origin of the global financial crisis."																					1	0	0
331141	BIS warns on debt; BNP Paribas braces for fine; Argentina angers judge  ...	http://www.interest.co.nz/news/70694/bis-warns-debt-bnp-paribas-braces-fine-argentina-angers-judge-bankers-trade-key-infrastru	Interest.co.nz	b	d_IY8r2JZTWLvkMrM33bhyNY2EkzM	www.interest.co.nz	2014-06-30 00:30:01	1		en	us0877,sold,key,judge,trading,infrastructure,weekend,million,economic,nz1,trade,ust,twi,bank,week,warns,debt,payment,paribas,settlements	"Here's my summary of the key news over the weekend in 90 seconds at 9 am, including news of a major asset bubble warning.

Buoyant financial markets are out of kilter with the shaky global economic and geopolitical outlook, the Bank for International Settlements said in its annual report published over the weekend. Crucially, it said "It is essential to move away from debt as the main engine of growth."

In Paris, BNP Paribas is preparing for the announcement of its penalty for breaking economic sanctions, which is expected to come very soon and be a fine of NZ$10 billion plus a ban of some interbank trading privileges.

Argentina is another with American legal woes. A US judge has ordered that a debt repayment made by Argentina to US bondholders be returned, calling the payment "an explosive action".

Argentina owes money to two sets of bondholders - those who have agreed a deal to restructure the debt, and those who have not. The judge previously ruled the country must pay both, but Friday's payment was just to those who had agreed a deal. The US legal system decides these things because the original debt was issued there and Argentina offered US law in any dispute.

Here's something you may not have known. We know about bankers buying up commodity positions, but you may not have known that ANZ owns four liquid fuels terminals in New Zealand, Auckland, Mt Maunganui, New Plymouth and Wellington. The ownership is in focus because ANZ has just sold them to Macquarie Bank along with four equivalent facilities in Australia. They hoped to get A$400 million for this key infrastructure business, but bidding was brisk; they sold for A$525 million, according to the AFR. Macquarie will want a return on that.

The transaction makes the point from the bank of International Settlements well. Asset bubbles grow and investors make dangerously risky decisions when interest rates are too low.

Benchmark UST 10 yr bond yields ended last week at 2.54%. Both oil and gold slipped a little in late Friday trading in New York.

We start the week at 87.7 USc, 93.2 AUc. The TWI is now at 81.5.

If you want to catch up with all the changes on Friday we have an update here.

The easiest place to stay up with today's event risk is by following our Economic Calendar here »"																					1	0	0
331144	BNP Paribas board approves record $8.9B settlement	http://www.cnbc.com/id/101798442	CNBC.com	b	d_IY8r2JZTWLvkMrM33bhyNY2EkzM	www.cnbc.com	2014-06-30 00:30:02	1			outlook,banking,zealands,zealand,policy,twoweek,low,record,trading,risks,rates	"5 Hours Ago

WELLINGTON, March 27- New Zealand's central bank kept interest rates at a record low of 1.75 percent on Wednesday and said increased downside risks to its outlook meant the next move in rates was now more likely to be a cut, knocking the currency to a two-week low. The New Zealand dollar was trading above $0.69 before the policy decision and immediately fell more..."																					1	0	0
331159	BNP Paribas to pay biggest-ever US fine on foreign bank	http://www.english.rfi.fr/americas/20140629-bnp-paribas-pay-biggest-ever-us-fine-foreign-bank	RFI	b	d_IY8r2JZTWLvkMrM33bhyNY2EkzM	www.english.rfi.fr	2014-06-30 00:30:06	1		en	president,pay,biggestever,fine,bnp,bank,sources,euros,fined,transactions,paribas,paris,billion,foreign	"France’s BNP Paribas has agreed to pay the biggest-ever fine imposed on a foreign bank by US regulators for breaking American sanctions against countries including Iran and Sudan, sources said Sunday.

Following months of tough negotiations, BNP has taken the unusual step for a company of pleading guilty and agreeing to pay the 8.9-billion-dollar (6.4-billion-euro) fine in order to avoid a trial, whose result would be uncertain.

Dossier: Eurozone in crisis

The sum is the equivalent of 16 months of the bank’s profits at 2013 levels and is far higher than the 1.1 billion euros it had set aside.

But it can afford to pay, given that it had 94.4 billion euros of funds in 2013.

In 2012 the US fined several foreign banks far less for the same offence.

The UK’s HSBC and Standard Chartered were fined 1.36 bilion euros and 483 million euros respectively and the Netherlands’ ING 446 million euros, while Crédit Suisse was fined 1.87 billion euros in May for incitement to tax evasion.

BNP is also expected to be forced to partially suspend its transactions in dollars, mainly relating to oil and gas carried on from offices in Paris, Geneva and Singapore, but it will have a period of grace in which to find another bank to carry out these operations.

The guilty plea could leave the bank open to damages claims from third parties and might mean US pension funds or local authorities have to close their accounts because of internatl regulations.

About a dozen employees, including former high-ranker Georges Chodron de Courcel, are to quit the bank, sources say.

The transactions were legal in an international law but actionable in the US because they were carried out in dollars or went through clearing houses there.

The French government is dismayed by the size of the fine and President François Hollande raised the question with US President Barack Obama when he visited Paris this month."																					1	0	0
331162	Bank chief warns of 'severe' punishment	http://www.thelocal.fr/20140629/bank-chief-warns-of-severe-punishment	The Local.fr	b	d_IY8r2JZTWLvkMrM33bhyNY2EkzM	www.thelocal.fr	2014-06-30 00:30:07	1		en	wrote,employees,severe,bank,week,worth,ties,french,chief,york,paribas,sanctions,punishment,billion,warns	""I want to be clear: we will be punished severely because malfunctions have occurred and mistakes were made," director general Jean-Laurent Bonnafe wrote to employees on Friday, French news channel i-Tele reported.



"But this difficulty we are facing will not impact our roadmap."



The New York Times reported on Friday that BNP Paribas is set to announce a deal next week to plead guilty to helping some countries avoid US sanctions and agree to pay an $8.9 billion (€6.4 billion) fine.



BNP Paribas is accused of breaching US sanctions against Iran, Sudan and Cuba between 2002 and 2009 by handling $30 billion (€22 billion) worth of transactions with them.



At the request of US authorities, the bank -- France's largest by capitalisation -- has already severed ties with a dozen employees, including two senior executives.



The case has strained ties between Paris and Washington, with the French government warning a mooted fine exceeding $10 billion (€7.2 billion)

would endanger negotiations on a US-EU free trade agreement and cause a knock-on effect through the banking system.



"																					1	0	0
334110	Housing Market Still Sluggish, Pending Home Sales on the Rise	http://sleekmoney.com/housing-market-still-sluggish-pending-home-sales-on-the-rise/118/	sleekmoney	b	d_gSOVyb6AktUYMCiBrZgMdhpbkTM	sleekmoney.com	2014-06-30 18:10:14	1		en	tools,market,trading,terms,purposes,does,marketbeat,data,research,advice,provided,ratings,stock,delayed,zacks	"© 2019 Market data provided is at least 10-minutes delayed and hosted by Barchart Solutions . Fundamental company data provided by Morningstar and Zacks Investment Research. Information is provided 'as-is' and solely for informational purposes, not for trading purposes or advice, and is delayed. To see all exchange delays and terms of use please see disclaimer

© American Consumer News, LLC dba MarketBeat® 2010-2019. All rights reserved.326 E 8th St #108, Sioux Falls, SD 57103 | [email protected] | (844) 978-6257MarketBeat does not provide financial advice and does not issue recommendations or offers to buy stock or sell any security. Learn more"																					1	0	0
361122	Khloe Kardashian: Boyfriend French Montana Is "Light and Easy" — "That's What  ...	http://www.wetpaint.com/khloe-kardashian/articles/2014-07-05-french-montana-light-easy-need	Wetpaint	e	d_IN4PZLvv_SpJMDYzo0e0OmAGQ0M	www.wetpaint.com	2014-07-05 22:42:35	1		en	picture,seriously,read,khloe,happy,big,thing,kardashian,finally,tristan	Khloe Kardashian finally made her big announcement and it is seriously the best thing ever. We're so happy for her and Tristan. See the picture here! Read More...																					1	0	0
361128	French Montana Takes His Luxury Rides to the Desert in his New Video	http://www.autoevolution.com/news/french-montana-takes-his-luxury-rides-to-the-desert-in-his-new-video-83506.html	autoevolution	e	d_IN4PZLvv_SpJMDYzo0e0OmAGQ0M	www.autoevolution.com	2014-07-05 22:42:37	1		en	fans,vehicles,rides,wear,luxury,montana,desert,french,video,videos,takes,rapper,wouldnt	Opulence and pride is what the average rapper video always has to be about, so of course French Montana surrenders to the game’s laws. Take Soulja Boy’s new “Tony Hawk” video , for instance. The 23-year old rapper had his Bentley Continental GT all dressed in red, which is the exact color your wouldn’t expect this high-class technology and performance package to wear. And then, at some point during the video, fans see him cooking $20 bills.Other rappers are more into the dark light type of videos, so they go for the gangsta black-and-white decor, having guns and murdered-out luxury vehicles in it. But whatever their style is, these artists almost every time will brag about their cars.It’s the case of French Montana as well, who has been posting a couple of pictures with him posing next to his gorgeous luxury cars somewhere in the dessert. According to his quotes, it seems he finally decided to film the video for the 2013-released hit “Julius Caesar.” So, all the fans out there, prepare to sit back and enjoy, because French Montana is days away from once again “invading” your TV screens.																					1	0	0
361134	Kim Kardashian's psychic predicts pregnancy	http://www.dailystar.co.uk/showbiz/goss/387387/Kim-Kardashian-s-psychic-predicts-pregnancy	Daily Star	e	d_IN4PZLvv_SpJMDYzo0e0OmAGQ0M	www.dailystar.co.uk	2014-07-05 22:42:38	1		en	sparks,tells,kardashian,trailer,no2,kuwtk,im,going,kimye,fall,really,pregnant,west,rumours,pregnancy,way,told,psychic,kim	"And we assume the bootiful babe and husband Kanye West, 37, will continue picking bizarre names for their offspring.

Kim Kardashian has said her psychic told her she’d fall pregnant soon.

“My psychic said I’m going to get pregnant really soon” Kim Kardashian

In a preview for Sunday’s episode of Keeping Up With The Kardashians, the reality star, 33, says: “My psychic said I’m going to get pregnant really soon.”

In the clip Kim, seen here heading out for lunch in the Hamptons, also had a cruel dig at sister Khloe, 30, who has spoken about her struggles to fall pregnant.

Kim tells her: “She said you should get a sperm donor and the guy will come later.” Charming."																					1	0	0
361138	Khloé Kardashian Hosts 30th Birthday Bash In Vegas	http://www.mtv.co.uk/khloe-kardashian/news/khloe-kardashian-continues-30th-birthday-celebrations-with-french-montana-in-vegas	MTV UK	e	d_IN4PZLvv_SpJMDYzo0e0OmAGQ0M	www.mtv.co.uk	2014-07-05 22:42:39	1		en	im,wanna,dont,hosts,khloé,play,kardashian,til,walk,birthday,bash,30th,tryna,save,niggas,vegas,fuckin	"View the lyrics

You wanted to fuckin' walk around these roaches

These niggas is roaches

These niggas is mere motherfuckin' mortals

I'm tryna push you to supreme bein'

You don't wanna motherfuckin'

You don't wanna embrace your destiny

You wanna get by

You don't wanna go into the motherfuckin' dark

Where it's lonely

You can't handle the motherfuckin', the pain

Of the motherfuckin' not knowin' when the shit is gonna stop



Mama's tryna save me

But she don't know I'm tryna save her

Man, them niggas tried to play me

Man, 'til I got this paper

You're nobody 'til somebody kills you



"Blast for me" -- the last words from my nigga

On the pavement, born killers, body shivers

Drug money, dollar figures

Hustlers moving out of rentals, art of war is mental

Having sushi down in Nobu

Strapped like an Afghan soldier, nowhere to go to

So it's bang, no survivors

Only riders on my rider, murder rate rises

Stalkin' niggas on their IG's, never; I be

Still solo, Under Armour still Polo

No wire, on fire

My desire for fine things made me a liar, a shooter

Gettin' high feeling like it's voodoo

Nine lives, SK with the cooler

Makaveli in the 'Rari, still B-I double G, I, E

I pray you smoke with me

Go to bed with a kilo like Casino

Janet Reno, we all we got the creed of Nino

Pretty cars in the driveway

If you cut it then you sideways, double up, crime pays



Mama's tryna save me

But she don't know I'm tryna save her

Man, them niggas tried to play me

Man, 'til I got this paper

You're nobody 'til somebody kills you



You fuckin' wanna walk around with these niggas?

What the fuck is their culture?

Where the fuck is their souls at?

What defines you?

These niggas with these fuckin' silly looks on their faces

You wanna walk around with them or you wanna walk with God, nigga?

Make up your got damn mind



I'm from where the streets test you

Niggas mix business and pleasure where the cocaine measure

The narcotics is our product

The by-product, you walk up on me, I cock it

New Mercedes as it peels off

Nothing penetrates the steel doors, gang signs, see 'em all

I said my prayer as I'm countin' sheep

Never really athletic, but I play for keeps, do you feel me?

The mortician, the morgue fillin' with more snitches

We kill 'em and taking their bitches, R.I.P

Chinchillas on a winter night

Black bottles when I'm feelin' like, you wanna know what winners like

And I'm never on that tour bus

Just a decoy for niggas, the PJ's for two of us

Ciroc boys down to die for Diddy

My niggas ride for less, keep it real, homie, made me filthy

Touch mine until it's even kill

Like I'm knowing every heathen will, closed the deal with Steven Hill

We Magic City of the networks

Cut a nigga cast off, how my nigga net worths



Mama's tryna save me

But she don't know I'm tryna save her

Man, them niggas tried to play me

Man, 'til I got this paper

You're nobody 'til somebody kills you



Fuck you wanna talk about?

Fuckin' jewelries and Bentley's and Hublot's

And fuckin' art that niggas ain't got on their fuckin' walls

And fuckin' mansions niggas ain't got

Niggas can't even pay the IRS, let alone their fuckin' staff, nigga

You gotta tell the truth, man

The truth'll set you free, son

The truth will set you free

Writer(s): SEAN PUFFY COMBS, CHRISTOPHER WALLACE, STEVEN A JORDAN, WILLIAM LEONARD ROBERTS, KARIM KHARBOUCH, JAMES ALEXANDER DAVID, OLIVER MARK DICKINSON, OTIS GEORGE JOHNSON, ETHRAM LOPEZ, JEAN LOUHSDON, BILLY PRESTON, YASMIN ZARINE SHAHMIR, CARL E THOMPSON Lyrics powered by www.musixmatch.com"																					1	0	0
361152	Khloé Kardashian & French Montana Dating Rumors 2014: Source Claims  ...	http://www.latinpost.com/articles/16418/20140704/khlo%C3%A9-kardashian-french-montana-dating-rumors-2014-source-claims-rapper.htm	Latin Post	e	d_IN4PZLvv_SpJMDYzo0e0OmAGQ0M	www.latinpost.com	2014-07-05 22:42:43	1		en	son,french,kardashians,father,rapper,khloé,hes,toy,kardashian,money,montana,reaching,man,source,child,rumors	"After French Montana was seen all over the news celebrating his new flame Khloé Kardashian's 30th birthday last weekend, a source close to his estranged wife Deen Kharbouch has opened up about the rapper's allweged indifference to his 4-year-old son Kruz.

The "Ballin Out" rapper recently splurged $100,000 on the "Keeping Up With the Kardashians" star for her big day.

"French has purchased a vehicle for someone who doesn't need it. But he's insisted that he would not pay for his child to go to school," the source told Radar Online in reference to the new $50,000 black Jeep he bought Kardashian. "He has never even bought Kruz as much as a toy ever since his shot to fame. This hurts beyond words what he did, does and continues to publicly do for the sake of fame and Kardashian money."

Deen had been P. Diddy's protégé since 2006 until she and Montana, who is signed to Bad Boys Records, started divorce proceedings in 2012. With that being said, the source revealed that the Moroccan emcee is simply spending money he does not have, even using his wife's money.

"He's [not just] blowing his money [but] his wife's money too! He's not a millionaire," the source said. "That's what he does. He makes other people think he's on top. He's a con man. And if the Kardashians are falling for that, that's his MO."

While flying to places with the reality star, the "I Ain't Worried About Nothin" hitmaker apparently has reportedly not called or visited his son in a while.

"Kruz has not seen or spoken to his father in over six months. Nor has his father inquired about Kruz's well-being in over six months," the insider claimed. "Since the fame, he's been a deadbeat. He also threw a birthday bash for this woman and did not attend his son's pre-school graduation. His son was the only child without a father present."

The tabloid website's source continued to criticize Montana's irresponsibility.

"Reports that were printed that claim French visits his son are complete rubbish," the source claimed. "Despite French living and being in New York City he has never spent a minute with his child. What you have here is complete abandonment."

The source then questioned French Montana's thoughtless "devastating" behavior on social media, saying the rapper "posted a monkey on Instagram versus his son. He calls other people family, but he never once asks about his son"

In addition, the insider accused Kardashian as well as her notorious family of being hypocrites.

"The irony is Khloé was the first to oppose her best friend Mallika's relationship with a married man on her show. She was an advocate for her not doing that and now she is doing the same thing," the source added. "I guess only the Kardashians deserve to have two-parent households. They preach 'family first,' but support a man that abandoned his wife and child completely. They enable him in doing so.""																					1	0	0
361156	French Montana Already Cheating on Khloe Kardashian? Intern Reveals  ...	http://www.inquisitr.com/1334609/french-montana-already-cheating-on-khloe-kardashian-intern-reveals-shocking-details-he-climbed-on-top-of-me/	The Inquisitr	e	d_IN4PZLvv_SpJMDYzo0e0OmAGQ0M	www.inquisitr.com	2014-07-05 22:42:45	1		en	tour,kardashian,interview,things,french,im,khloe,montana,climbed,rapper,reportedly,took,shocking,reveals,sanchez,details,cheating,went,intern	"French Montana has been dating Khloe Kardashian for a couple of months now. The two have been seen together quite often lately, even engaging in shameless PDA without a care in the world. They two have exchanged lavish gifts, and been on a number clandestine getaways.

The Keeping Up with the Kardashians star has been floating on cloud nine. However, if the most recent media reports are true, things could change between her and the Excuse My French rapper rather quickly.

According to Radar Online, the 29-year-old rapper reportedly isn’t as faithful as he wants his girlfriend to think. As a matter of fact, there’s a woman who has openly admitted that French tried to come on to her!

Mariela Sanchez, a 23-year-old intern journalist for Kiss 108 radio show, Matty in the Morning recounted her time with the rapper. Although she claims she only wanted an interview, French wanted much more. During an exclusive, on-air interview with the station, Sanchez explained that she went to the Centro Nightclub where French performed on Friday, June 20 in Lawrence, Massachusetts. She was reportedly escorted to the VIP section of the club after the show and introduced to the “Ain’t Worried Bout Nothin'” rapper.

Although she was relatively eager to land the interview, and ultimately agreed to speak with him on his tour bus, she explained that things quickly took an unexpected turn. Once inside of the tour bus, French reportedly offered to fly her out to New York to spend time with him.

He even took things a step further by suggesting they finish their discussion in the lobby of the hotel where he was staying. Although Sanchez reportedly declined his advances, French wasn’t deterred because things went event even further. She alleges that the “Freaks” rapper actually “climbed on top of her.”

“All of his boys leave the tour bus and he climbs on top of me. I’m like, ‘I’m not about this life. I have morals. I have a lot to lose. I want to be in the industry, and I’m not going to start out in the industry in the wrong way.'”

Sanchez went on to explain that French downplayed the entire incident by saying that she was going to eventually “one of these broke guys” anyway, so why not him?” He also took time to mention his girlfriend, Khloe, as a way of clarifying their encounter wouldn’t be personal. “You know I have a girlfriend,” he said.

Once French reportedly made one last attempt to take advantage of Sanchez, she revealed that she had to forcefully push him away using both hands.

Do you believe Sanchez’s claim or is French a faithful?

[Image(s) via Bing]"																					1	0	0
372178	Facebook Deletes Cheerleader's Photos of Poached Animals After Outcry	http://www.newsmax.com/US/Facebook-cheerleader-slain-animals/2014/07/08/id/581424/	Newsmax.com	t	d_juLkg3r8v6KPMXADmR3uNqSZobM	www.newsmax.com	2014-07-09 13:21:07	1			outcry,deletes,hunted,solicitation,pioneering,photos,prostituti,samples,animals,robert,regard,trump,russia,plea,facebook,cheerleaders,patriots	"You May Also Like

President Donald Trump might have committed obstruction of justice in regard to the Russia investigation, according to n . . .

New England Patriots owner Robert Kraft on Tuesday entered a not guilty plea to two counts of solicitation of prostituti . . .

A pioneering use of drones to fly blood samples across a North Carolina hospital campus launched Tuesday in the latest m . . ."																					1	0	0