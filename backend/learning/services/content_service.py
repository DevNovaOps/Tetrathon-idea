from learning.models import Course, Lesson, Quiz, Article, AiTip

class ContentService:
    @staticmethod
    def seed_all_content():
        courses_created = ContentService.seed_courses()
        articles_created = ContentService.seed_articles()
        tips_created = ContentService.seed_tips()
        ContentService.update_existing_content()
        return {
            "courses": courses_created,
            "articles": articles_created,
            "tips": tips_created
        }

    @staticmethod
    def update_existing_content():
        category_videos = {
            "Featured Course": "https://www.youtube.com/embed/p7HKvqRI_Bo",
            "What is Credit Score?": "https://www.youtube.com/embed/V9B4b2j8g7c",
            "Mutual Funds": "https://www.youtube.com/embed/WJ12X0Xb6y4",
            "SIPs": "https://www.youtube.com/embed/ruxLdbvL_yA",
            "Emergency Fund": "https://www.youtube.com/embed/6T2H4G9V1t0",
            "Financial Literacy": "https://www.youtube.com/embed/X9hA-S23l1M",
            "Budgeting": "https://www.youtube.com/embed/6T2H4G9V1t0",
            "Stock Market Basics": "https://www.youtube.com/embed/p7HKvqRI_Bo",
            "Tax Planning": "https://www.youtube.com/embed/7Q25-STIZTs",
            "Financial Security": "https://www.youtube.com/embed/sdpxddDzXfE",
        }
        for course in Course.objects.all():
            vid_url = category_videos.get(course.category, "https://www.youtube.com/embed/p7HKvqRI_Bo")
            for lesson in course.lessons.all():
                if lesson.video_url == "https://www.youtube.com/embed/dQw4w9WgXcQ" or not lesson.video_url:
                    lesson.video_url = vid_url
                    lesson.save()

        article_urls = {
            "How Credit Scores Work": "https://zerodha.com/varsity/chapter/credit-score-and-credit-reports/",
            "Top 10 Saving Habits": "https://zerodha.com/varsity/module/personal-finance/",
            "Investment Mistakes to Avoid": "https://zerodha.com/varsity/chapter/common-mistakes-in-investing/",
            "Understanding Compound Interest": "https://www.investopedia.com/terms/c/compoundinterest.asp",
            "Financial Planning for Beginners": "https://zerodha.com/varsity/chapter/introduction-to-personal-finance/",
            "Mutual Fund Direct vs Regular Plans": "https://zerodha.com/varsity/chapter/mutual-fund-schemes/",
            "How to Read Your CIBIL Report": "https://www.cibil.com/faq/understand-your-credit-score"
        }
        for art in Article.objects.all():
            if not art.url and art.title in article_urls:
                art.url = article_urls[art.title]
                art.save()

    @staticmethod
    def seed_courses():
        if Course.objects.count() > 0:
            return 0

        category_videos = {
            "Featured Course": "https://www.youtube.com/embed/p7HKvqRI_Bo",
            "What is Credit Score?": "https://www.youtube.com/embed/V9B4b2j8g7c",
            "Mutual Funds": "https://www.youtube.com/embed/WJ12X0Xb6y4",
            "SIPs": "https://www.youtube.com/embed/ruxLdbvL_yA",
            "Emergency Fund": "https://www.youtube.com/embed/6T2H4G9V1t0",
            "Financial Literacy": "https://www.youtube.com/embed/X9hA-S23l1M",
            "Budgeting": "https://www.youtube.com/embed/6T2H4G9V1t0",
            "Stock Market Basics": "https://www.youtube.com/embed/p7HKvqRI_Bo",
            "Tax Planning": "https://www.youtube.com/embed/7Q25-STIZTs",
            "Financial Security": "https://www.youtube.com/embed/sdpxddDzXfE",
        }

        # Featured Course & Categories
        categories_data = [
            {
                "title": "Master Personal Finance",
                "category": "Featured Course",
                "difficulty": "Beginner",
                "hours": 4.0,
                "thumbnail": "📘",
                "desc": "A comprehensive beginner-friendly course covering budgeting, saving, investing, and building long-term financial security.",
                "lessons": [
                    {"title": "The Foundation of Financial Independence", "duration": 20, "content": "Learn why personal finance is 80% behavior and 20% knowledge. We explore how tracking every rupee builds the foundation for long-term wealth compounding."},
                    {"title": "The 50/30/20 Budgeting Rule", "duration": 20, "content": "Master the simple framework of allocating 50% of income to needs, 30% to wants, and 20% directly to wealth building and debt reduction."},
                    {"title": "Building Your First Emergency Shield", "duration": 15, "content": "Discover why keeping 6 months of living expenses in a liquid savings account protects your long-term equity investments from forced liquidation."},
                ]
            },
            {
                "title": "What is Credit Score?",
                "category": "What is Credit Score?",
                "difficulty": "Beginner",
                "hours": 1.5,
                "thumbnail": "🛡️",
                "desc": "Understand how credit score works, why CIBIL matters, and how to maintain an 800+ rating.",
                "lessons": [
                    {"title": "Decoding Your CIBIL Report", "duration": 20, "content": "Your CIBIL score ranges from 300 to 900. Lenders evaluate this 3-digit number to determine loan eligibility and interest rates."},
                    {"title": "The 30% Credit Utilization Secret", "duration": 25, "content": "Using more than 30% of your available credit card limit signals credit hunger to credit bureaus and temporarily depresses your score."},
                    {"title": "Never Miss a Due Date", "duration": 20, "content": "Payment history accounts for 35% of your total credit score calculation. Setting up automated debit mandates eliminates late payment penalties."},
                    {"title": "Handling Credit Mix and Inquiries", "duration": 25, "content": "A healthy mix of secured loans (like home loans) and unsecured loans (like credit cards) boosts credit credibility."},
                ]
            },
            {
                "title": "Mutual Funds Explained",
                "category": "Mutual Funds",
                "difficulty": "Intermediate",
                "hours": 2.5,
                "thumbnail": "📊",
                "desc": "Learn about mutual funds, asset management companies, expense ratios, and equity vs debt schemes.",
                "lessons": [
                    {"title": "How Mutual Funds Pool Wealth", "duration": 30, "content": "Mutual funds collect money from thousands of investors and professionally deploy it across diversified stocks and bonds."},
                    {"title": "Large Cap vs Mid Cap vs Small Cap", "duration": 30, "content": "Large cap funds invest in top 100 established companies offering stability, while small cap funds target high growth potential with higher volatility."},
                    {"title": "Understanding Expense Ratio and TER", "duration": 25, "content": "The Total Expense Ratio (TER) is the annual fee charged by mutual funds. Even a 0.5% lower expense ratio in Direct plans saves lakhs over 20 years."},
                    {"title": "Direct Plans vs Regular Plans", "duration": 30, "content": "Direct plans bypass distributor commissions, generating 1% to 1.5% extra compounded annual growth compared to regular plans."},
                    {"title": "Taxation of Mutual Funds in India", "duration": 35, "content": "Understand Short Term Capital Gains (STCG) and Long Term Capital Gains (LTCG) tax rules for equity and debt mutual funds."},
                ]
            },
            {
                "title": "Mastering SIPs",
                "category": "SIPs",
                "difficulty": "Beginner",
                "hours": 1.0,
                "thumbnail": "💰",
                "desc": "Everything about Systematic Investment Plans, rupee cost averaging, and compounding power.",
                "lessons": [
                    {"title": "The Magic of Rupee Cost Averaging", "duration": 20, "content": "By investing a fixed sum every month via SIP, you automatically buy more units when market prices fall and fewer units when prices rise."},
                    {"title": "The 8th Wonder: Compound Interest", "duration": 20, "content": "Albert Einstein called compound interest the 8th wonder of the world. An SIP of ₹10,000 for 20 years at 12% grows to over ₹99 Lakhs."},
                    {"title": "Step-Up SIPs: Boosting Growth with Income", "duration": 20, "content": "Increasing your SIP contribution by just 10% annually alongside your salary increments can double your final retirement corpus."},
                ]
            },
            {
                "title": "Building an Emergency Fund",
                "category": "Emergency Fund",
                "difficulty": "Beginner",
                "hours": 1.0,
                "thumbnail": "🛟",
                "desc": "Why an emergency fund is your financial bedrock and where to safely park your liquid cash.",
                "lessons": [
                    {"title": "Why 6 Months of Expenses is Mandatory", "duration": 20, "content": "Medical emergencies or job transitions happen without warning. An emergency fund ensures you never break your long-term compounding investments."},
                    {"title": "Liquid Mutual Funds vs Savings Accounts", "duration": 20, "content": "Learn how liquid mutual funds offer higher post-tax yield than traditional bank savings accounts while maintaining 24-hour instant redemption."},
                    {"title": "Avoiding the Temptation to Spend", "duration": 20, "content": "Your emergency fund must be kept in a separate, dedicated bank account without linked debit card shopping privileges."},
                ]
            },
            {
                "title": "Essential Financial Literacy",
                "category": "Financial Literacy",
                "difficulty": "Beginner",
                "hours": 3.0,
                "thumbnail": "📖",
                "desc": "Basic financial concepts, inflation, time value of money, and banking essentials everyone should know.",
                "lessons": [
                    {"title": "Understanding Inflation: The Silent Thief", "duration": 30, "content": "Inflation erodes purchasing power at 6% annually. If your money is sitting in a 3% savings account, you are losing real wealth every single day."},
                    {"title": "Good Debt vs Bad Debt", "duration": 30, "content": "Good debt generates income or appreciates in value (like an education or business loan), whereas bad debt drains cash flow on depreciating consumer goods."},
                    {"title": "The Rule of 72", "duration": 25, "content": "Divide 72 by your annual interest rate to instantly calculate how many years it will take for your investment money to double."},
                    {"title": "Understanding Net Worth", "duration": 30, "content": "Net worth is simply total assets minus total liabilities. Tracking net worth quarterly is the ultimate scorecard of financial progress."},
                    {"title": "Health Insurance and Life Insurance Basics", "duration": 35, "content": "Never mix insurance and investment. Buy pure term life insurance for protection and comprehensive health insurance for family hospitalization."},
                    {"title": "Avoiding Common Financial Scams", "duration": 30, "content": "How to spot Ponzi schemes, unauthorized phishing apps, and get-rich-quick crypto traps that promise guaranteed unrealistic daily returns."},
                ]
            },
            {
                "title": "Smart Budgeting Methods",
                "category": "Budgeting",
                "difficulty": "Beginner",
                "hours": 2.0,
                "thumbnail": "💳",
                "desc": "How to budget, track expenses, eliminate cash leaks, and achieve monthly savings targets.",
                "lessons": [
                    {"title": "Zero-Based Budgeting", "duration": 30, "content": "Assign every single rupee a specific job before the month begins, ensuring your total income minus expenses and savings equals exactly zero."},
                    {"title": "The Envelope Method in the Digital Age", "duration": 30, "content": "How to use digital sub-accounts and automated transfers to cap discretionary spending on dining out, shopping, and entertainment."},
                    {"title": "Auditing Monthly Subscriptions", "duration": 30, "content": "Unused OTT subscriptions, gym memberships, and auto-renewing apps silently drain thousands of rupees annually. Here is how to conduct a 15-minute subscription audit."},
                    {"title": "Managing Irregular Income", "duration": 30, "content": "Budgeting strategies for freelancers, consultants, and variable commission earners by calculating baseline survival expenses."},
                ]
            },
            {
                "title": "Stock Market Basics",
                "category": "Stock Market Basics",
                "difficulty": "Intermediate",
                "hours": 2.5,
                "thumbnail": "📈",
                "desc": "Introduction to equities, stock exchanges (NSE/BSE), fundamental analysis, and long-term investing.",
                "lessons": [
                    {"title": "What is a Share of Stock?", "duration": 30, "content": "When you buy a share of stock, you become a part-owner of a real business, entitled to a proportional share of its future earnings and dividends."},
                    {"title": "Understanding NSE, BSE, and SEBI", "duration": 30, "content": "Learn how the National Stock Exchange and Bombay Stock Exchange facilitate electronic trading under the regulatory oversight of SEBI."},
                    {"title": "Price to Earnings (P/E) Ratio Explained", "duration": 30, "content": "The P/E ratio compares a company's current share price to its per-share earnings, helping you evaluate whether a stock is undervalued or expensive."},
                    {"title": "Dividends and Share Buybacks", "duration": 30, "content": "How mature companies return surplus cash flows to loyal shareholders through quarterly dividend payouts and open-market buybacks."},
                    {"title": "The Psychology of Market Crashes", "duration": 30, "content": "Market corrections are normal historical events. Successful investors view market dips as discount sales rather than reasons to panic sell."},
                ]
            },
            {
                "title": "Tax Planning Strategies",
                "category": "Tax Planning",
                "difficulty": "Advanced",
                "hours": 1.5,
                "thumbnail": "🏛️",
                "desc": "Save more through smart tax strategies, Section 80C, NPS, ELSS mutual funds, and new vs old regimes.",
                "lessons": [
                    {"title": "Maximizing Section 80C and ELSS", "duration": 30, "content": "Equity Linked Savings Schemes (ELSS) offer the shortest lock-in period of just 3 years among all 80C tax-saving options while delivering equity returns."},
                    {"title": "National Pension System (NPS) Benefits", "duration": 30, "content": "Claim an additional ₹50,000 tax deduction under Section 80CCD(1B) above the standard 80C limit by investing in low-cost NPS retirement funds."},
                    {"title": "Old Tax Regime vs New Tax Regime", "duration": 30, "content": "A detailed mathematical comparison to help you choose whether the lower tax slabs of the new regime beat the customized deductions of the old regime."},
                ]
            },
            {
                "title": "Financial Security & Identity Protection",
                "category": "Financial Security",
                "difficulty": "Intermediate",
                "hours": 2.0,
                "thumbnail": "🔐",
                "desc": "Protect your wealth, secure online banking, understand nominees, and prevent identity theft.",
                "lessons": [
                    {"title": "Why Every Account Must Have a Nominee", "duration": 30, "content": "Without proper registered nominees on bank accounts and demat folios, transferring assets to grieving family members requires arduous legal succession certificates."},
                    {"title": "Two-Factor Authentication and Password Vaults", "duration": 30, "content": "Securing your financial emails and banking apps with hardware keys or authenticator apps instead of SMS OTPs prevents SIM-swap fraud."},
                    {"title": "Creating a Digital Financial Will", "duration": 30, "content": "How to securely document all your passwords, insurance policies, and mutual fund folios in an encrypted vault accessible to trusted family members."},
                    {"title": "Monitoring Credit Reports for Fraud", "duration": 30, "content": "Regularly checking your free annual credit report from CIBIL and Experian helps you immediately catch unauthorized loan accounts opened in your name."},
                ]
            }
        ]

        count = 0
        for cat in categories_data:
            course = Course.objects.create(
                title=cat["title"],
                description=cat["desc"],
                difficulty=cat["difficulty"],
                category=cat["category"],
                thumbnail=cat["thumbnail"],
                estimated_hours=cat["hours"],
                total_lessons=len(cat["lessons"])
            )
            count += 1
            vid_url = category_videos.get(cat["category"], "https://www.youtube.com/embed/p7HKvqRI_Bo")
            for idx, l in enumerate(cat["lessons"], 1):
                lesson = Lesson.objects.create(
                    course=course,
                    title=l["title"],
                    content=l["content"],
                    duration=l["duration"],
                    order=idx,
                    video_url=vid_url,
                    article=f"### Comprehensive Study Guide: {l['title']}\n\n{l['content']}\n\n**Key Takeaway**: Apply this principle immediately to strengthen your personal financial health."
                )
                # Create a quiz for this lesson
                Quiz.objects.create(
                    lesson=lesson,
                    question=f"What is the core principle taught in '{l['title']}'?",
                    options=[
                        "Consistent discipline and proactive financial planning lead to long-term compounding growth.",
                        "Ignoring expenses and borrowing high-interest consumer loans is the fastest way to wealth.",
                        "Financial planning is only useful for people who are already millionaires.",
                        "Keeping all cash hidden at home protects against inflation."
                    ],
                    correct_answer=0,
                    explanation="Consistent discipline, automated saving habits, and understanding financial rules are essential for wealth compounding.",
                    marks=30
                )
        return count

    @staticmethod
    def seed_articles():
        if Article.objects.count() > 0:
            return 0
        articles = [
            {"title": "How Credit Scores Work", "tag": "Credit", "color": "blue-tag", "time": "5 min read", "diff": "Beginner", "url": "https://zerodha.com/varsity/chapter/credit-score-and-credit-reports/", "summary": "Understand the 5 key factors that impact your CIBIL score.", "content": "Your credit score is evaluated based on payment history (35%), credit utilization (30%), length of credit history (15%), credit mix (10%), and new credit inquiries (10%). Maintaining utilization strictly under 30% and automating payments are the two fastest ways to build an 800+ rating."},
            {"title": "Top 10 Saving Habits", "tag": "Saving", "color": "green-tag", "time": "4 min read", "diff": "Beginner", "url": "https://zerodha.com/varsity/module/personal-finance/", "summary": "Simple habits that can help you save ₹5,000+ per month.", "content": "Automating your savings transfer on salary day, packing homemade lunch, auditing recurring subscriptions, and using the 24-hour rule before major purchases can save thousands. Treat your monthly savings as a non-negotiable expense."},
            {"title": "Investment Mistakes to Avoid", "tag": "Investing", "color": "orange-tag", "time": "6 min read", "diff": "Intermediate", "url": "https://zerodha.com/varsity/chapter/common-mistakes-in-investing/", "summary": "Common pitfalls every new investor should watch out for.", "content": "Never invest based on hot stock tips from social media, avoid stopping SIPs during market dips, and always check expense ratios before buying regular mutual fund schemes. Stay consistent with index funds and direct equity mutual funds."},
            {"title": "Understanding Compound Interest", "tag": "Growth", "color": "purple-tag", "time": "3 min read", "diff": "Beginner", "url": "https://www.investopedia.com/terms/c/compoundinterest.asp", "summary": "The 8th wonder of the world — and how to use it.", "content": "Compounding means earning interest on your interest. Starting at age 25 instead of age 35 with the same monthly amount can result in 3x more wealth at retirement due to exponential compounding."},
            {"title": "Financial Planning for Beginners", "tag": "Planning", "color": "cyan-tag", "time": "7 min read", "diff": "Beginner", "url": "https://zerodha.com/varsity/chapter/introduction-to-personal-finance/", "summary": "A step-by-step guide to securing your financial future.", "content": "Step 1: Get term and health insurance. Step 2: Build a 6-month emergency fund in a liquid fund. Step 3: Clear high-interest credit card debt. Step 4: Start an equity SIP for retirement."},
            {"title": "Mutual Fund Direct vs Regular Plans", "tag": "Investing", "color": "emerald-tag", "time": "6 min read", "diff": "Intermediate", "url": "https://zerodha.com/varsity/chapter/mutual-fund-schemes/", "summary": "Why saving distributor commissions generates lakhs in extra returns.", "content": "Direct mutual fund plans bypass distributor commissions, resulting in a 1% to 1.5% lower Total Expense Ratio (TER). Over a 20-year investment horizon, this difference compounds into lakhs of additional wealth."},
            {"title": "How to Read Your CIBIL Report", "tag": "Credit", "color": "blue-tag", "time": "5 min read", "diff": "Beginner", "url": "https://www.cibil.com/faq/understand-your-credit-score", "summary": "Step-by-step instructions for checking DPD and credit inquiries.", "content": "Check your Days Past Due (DPD) section to ensure all entries show '000' (on-time payment). If you see any unauthorized loan accounts or hard credit inquiries you did not initiate, dispute them immediately on the CIBIL portal."}
        ]
        for a in articles:
            Article.objects.create(
                title=a["title"], tag=a["tag"], tag_color=a["color"],
                read_time=a["time"], difficulty=a["diff"], summary=a["summary"], content=a["content"], url=a.get("url", "")
            )
        return len(articles)

    @staticmethod
    def seed_tips():
        if AiTip.objects.count() > 0:
            return 0
        tips = [
            {"title": "Complete one lesson daily", "content": "Consistency beats intensity. Aim for 15 minutes of learning every day.", "icon": "💡", "bg": "green-bg", "cat": "General"},
            {"title": "Review budgeting concepts", "content": "Revisit the 50/30/20 rule and apply it to your current spending.", "icon": "📘", "bg": "blue-bg", "cat": "Budgeting"},
            {"title": "Start learning about SIPs", "content": "Understanding systematic investment plans is key to long-term wealth.", "icon": "📊", "bg": "purple-bg", "cat": "SIPs"},
            {"title": "Improve your financial literacy gradually", "content": "Focus on one topic per week to build strong foundational knowledge.", "icon": "🎯", "bg": "orange-bg", "cat": "Financial Literacy"},
        ]
        for t in tips:
            AiTip.objects.create(
                title=t["title"], content=t["content"], icon=t["icon"], icon_bg=t["bg"], category=t["cat"]
            )
        return len(tips)
