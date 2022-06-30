# Bay Area Housing - What is affordable?

I started this project to answer the question "which houses, if any, can someone afford in the Bay Area?" Obviously, this question has a lot of subjective and objective answers. I believe the best way to be close to objective is to "talk numbers" and to be as transparent as possible about what I am doing and why.

### Background
This project started in response to the [Stanford Affordability Task Force](https://affordability.stanford.edu/), which was created in 2018. In the four years since it’s creation it has yet to define what it means by affordability, or what makes something affordable. From digging through their website and through my emails it seems the process implemented by the task force is to send out surveys and try to improve future survey results. This does not strike me as an actionable performance objective - it is not the right way to approach a challenge like affordability. I believe the correct approach is to set performance goals and develop actions and metrics to track progress towards goals.

Of course to set goals and define actions and metrics I need some idea what it means to be “affordable”. To me affordability is obviously an economic challenge: there is a market and there are options with tradeoffs. For example, some people absolutely must raise emus in their backyard, or have 4 bedrooms and an office, or will not be able to sleep without an upstairs neighbor. While there are many possible tradeoffs I look at only two: single family homes and commute times to work (I use where I work). The reason I focus on single family homes because they are the ‘American Dream’. Home ownership is ingrained in Americans through our parents, politics and popular culture. It is also the primary method for families to [build intergenerational wealth](https://books.google.com/books?hl=en&lr=&id=TRt8CwAAQBAJ&oi=fnd&pg=PP1&dq=home+ownership+build+wealth&ots=KyHtC7xiXs&sig=kZbFoz_CUSCmTk54MVPIvoCT8EA#v=onepage&q=home%20ownership%20build%20wealth&f=false). I compare this to commute times because it is the primary method by which families can reach their home ownership goals. If one cannot afford that 4-bedroom house you need near work, maybe they can afford it one town over.

(Affordability is also a social challenge, but that is a fraught topic that I’m even less qualified to discuss.)

### What do governmental organizations say about affordability?
The US Government [Department of Housing and Urban Development](https://archives.hud.gov/local/nv/goodstories/2006-04-06glos.cfm) define affordable is the total cost of shelter that is <=30\% of gross income (what you are paid before any taxes or deductions are paid). The [State of California agrees](https://calbudgetcenter.org/app/uploads/2019/04/Report_California-Housing-Affordability-Crisis-Hits-Renters-and-Households-With-the-Lowest-Incomes-the-Hardest_04.2019.pdf). Use of a percentage makes sense because when it costs more to live in an area you have to pay more to do things like stock shelves, work gas stations or be teachers or firefighters.

### Housing prices are not mysterious
In this work I exmine the relationship between the cost of housing and salaries in the Bay Area in general and SLAC/Stanford in specific. I find that housing prices are (unsurprisingly) driven by scarcity and wages. In a market we can expect that, in general, existing items will go to the highest bidders. So if the number of houses available is N_h and the distribution of incomes in the local area is r(I) then the houses will goto the top end of the income distribution:
$$ N_{h}=\int_n^{\infty}r(I)\mathrm{d}I. $$
In this equation "n" is the lowest salary that can afford a house.

#### Wages in the bay area
I started by looking at salary distributions for new offers on [levels.fyi](www.levels.fyi). I chose this site for two reasons: 1) salaries and offers are (purportedly) verified and 2) they have submission dates. Other websites have been aggregating data for so long that it isn't clear how new the data is or who is being represented by the data. Levels.fyi tells you how old the data is. Wage data for "Hardware Professionals" in the Bay Area, including SLAC/Stanford, looks as follows:
<img width="628" alt="image" src="https://user-images.githubusercontent.com/8341540/176578499-2b40980e-31e7-4f5e-a8cb-0af84ef7d490.png">

Where direct compensation means money paid directly to the employee (wages, stock, bonus) but does not include this like health care, insurance or PTO. I've called out specific levels for people with a PhD at SLAC because I believe these people closely match the "hardware professionals" on levels.fyi. For reference, Grade I is a two or three year fixed term position, Grade K is a 5 year fixed term position and Grades L & M is "continuing" term position. So after a PhD and 7 years of experience a SLAC employee finds themselves behind the Bay Area median by $90,000/year. In specific the median wage is $220k/year.

#### Housing is scarce
So SLAC/Stanford employees are behind the curve on pay, but that wouldn't matter if there was plenty of housing (n < SLAC salaries). As is well known, there isn't sufficient housing. It is possible to dig up some numbers on how many single family homes are available. On March 28th, 2022:
* Santa Clara has 491 single family homes, median price is $1,825,000
* San Mateo has 271 single family homes, median price is $2,388,000
* There are 427 single family homes within 27.6 minutes of SLAC, median price $2,750,000.
<img width="560" alt="image" src="https://user-images.githubusercontent.com/8341540/176579976-85f4c42d-8c87-4565-a289-c5cad9b5d903.png">

Where [27.6 minutes](https://www.census.gov/newsroom/press-releases/2021/one-way-travel-time-to-work-rises.html) is the national average for commute times. SLAC turned over 400 people in the last two years. At an average rate or 17 new people per month (though I doubt all of them are new to the Bay Area) SLAC employees are looking to snap up 2% (17/762) of the available houses near where they work. This last point is very handwavey order-of-magnitude calculation, I'm a physicist, we do that. The point is that 762 houses is an insufficient number of houses for two counties (Santa Clara and San Mateo) that have a combined population of 2.689 million people.

#### Who can afford those houses?
The last piece of the puzzle then is to answer "who can afford the housing that is available?" To answer this quesiton I had to roll up the cost of interest on a mortgage, property taxes, maintenance and even calculate the mortgage interest deduction for tax purposes. Then I calculate the direct compensation required to buy a home as follows:
<img width="998" alt="image" src="https://user-images.githubusercontent.com/8341540/176581931-c4f7b01f-1c44-42a3-8424-0e2d82fe8f84.png">

The wiggles in the line are the optimizer I use to solve the problem of inverting the monotonic piecewise continuous function that is federal tax brackets. I do not include California taxes. I poked around county tax websites and found taxes are something like 1.15\%. This assumes the buyer can put 20\% (a totally different story), and thus there is no PMI. I include a range of mortgage interest rates as a sort of error bar - they give a feel for how prices or income requirements change.

This plot can be read as follows:
The median home price in Santa Clara county is $1,825,000, that is the red line that says "Santa Clara". If mortgage interest rates are 3\% (solid black line) then a buyer would need ~$350k/year in income to afford the median house in Santa Clara. That same buyer with $350k/year income could "only" afford a $1,400,000 house if interest rates reach 7\% (dot dashed line). (If you're an economist you turn every plot sideways and could say that wages are sticky and that the median housing price in Santa Clara should drop to $1,400,000 as interest rates rise to 7%).

To afford that $1,825,000 house a buyer would need ~$400k/year. In San Mateo that number jumps to ~$525k/year. In the immediate area around SLAC/Stanford it goes even higher to >$600k/year. It is pretty obvious from the wages chart above that a couple making the median salary of $440k/year (2 x $220k/year) can easily afford the houses in Santa Clara and with a few more years experience get into San Mateo or even Palo Alto. It doesn't take many people, there aren't that many houses for sale.


