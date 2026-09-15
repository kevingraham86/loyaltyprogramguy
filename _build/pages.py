"""Generate the content pages (industries, guides, about), llms.txt and sitemap.xml.

Run from the repo root:   python3 _build/pages.py
Edit page content in PAGES below, re-run, commit the generated files.
Note: the repo has .nojekyll, so GitHub Pages publishes this file too. Never put secrets here.
"""
import json
import os
from datetime import date
from html import escape

SITE = "https://loyaltyprogramguy.com"
TODAY = date.today().isoformat()
PHONE_DISPLAY = "858-218-6905"
PHONE_E164 = "+18582186905"
CALENDLY = "https://calendly.com/smbaipartners"
GA_ID = "G-N7JTY70D7C"

PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#kevin",
    "name": "Kevin Graham",
    "jobTitle": "Customer Loyalty Program Consultant",
    "url": f"{SITE}/about/",
    "image": f"{SITE}/images/kevin-graham-headshot.jpg",
    "worksFor": {"@type": "Organization", "name": "SMB AI Partners"},
}

# --------------------------------------------------------------------------------------
# Page content. body is raw HTML. faqs feed both the visible FAQ and FAQPage schema.
# --------------------------------------------------------------------------------------
PAGES = [
    # ---------------------------------------------------------------- industries
    {
        "path": "restaurants/",
        "kind": "industry",
        "nav": "Restaurants",
        "title": "Text Loyalty Programs for Restaurants in San Diego | Loyalty Program Guy",
        "h1": "Text Message Loyalty Programs for Restaurants",
        "description": "How San Diego restaurants and cafés use automated text loyalty programs to fill slow nights, bring diners back, and earn more reviews. Local setup by Kevin Graham.",
        "answer": "A text message loyalty program gives restaurant guests a reason to come back: they check in with their phone number, earn rewards automatically, and get timely offers like a bounce-back deal, a birthday treat, or a “we miss you” text when they haven't visited in a while. You own the list, and the campaigns run on their own.",
        "body": """
<h2>Why repeat guests matter more than new ones</h2>
<p>Most restaurants spend on ads, delivery apps, and social posts to win a first visit, then have no system to earn the second. That second visit is where the money is. Research published in <em>Harvard Business Review</em> found acquiring a new customer can cost 5 to 25 times more than keeping an existing one, and Bain &amp; Company research found a 5% lift in retention can raise profits by 25% to 95%.</p>

<h2>What the program does for a restaurant</h2>
<ul>
  <li><strong>Bounce-back offer:</strong> a new member gets an incentive to return while the first meal is still fresh in their mind.</li>
  <li><strong>Digital punch card:</strong> “Your 8th visit is on us” without paper cards that get lost.</li>
  <li><strong>“We miss you” texts:</strong> automatically sent when a regular hasn't been in for the number of days you choose.</li>
  <li><strong>Birthday and anniversary rewards:</strong> a personal reason to book a table.</li>
  <li><strong>Slow-night blasts:</strong> send a Tuesday special at 3 p.m. and fill seats that night.</li>
  <li><strong>Review requests:</strong> after a repeat visit, happy guests get a direct link to leave a review.</li>
</ul>

<h2>Run the numbers for a restaurant</h2>
<div class="example">
  <p>Example: 800 guests on your list × $25 average ticket × half an extra visit per month</p>
  <p class="big">≈ $10,000 more per month</p>
  <p class="note">An illustration, not a promise. Your list size, offers, and how actively staff invite guests to join drive the result. <a href="/card/">Try your own numbers</a>.</p>
</div>

<h2>Ideas that work well for restaurants</h2>
<ul>
  <li>A free appetizer or drink on the second visit within 30 days.</li>
  <li>“Happy hour starts in 1 hour” texts on slow afternoons.</li>
  <li>A free dessert during a member's birthday week.</li>
  <li>First look at new menu items or seasonal specials for members.</li>
</ul>

<h2>How setup works</h2>
<p>I install the check-in kiosk and table and counter signs in person, set up your campaigns, and train your staff on how to invite guests to join. After launch, we review your numbers together every month. See <a href="/guides/sms-loyalty-program-cost/">what a program costs</a> or <a href="/guides/win-back-text-examples/">example texts that bring guests back</a>.</p>
""",
        "faqs": [
            ("Will guests think the texts are spam?", "No, as long as the program is opt-in and useful. Guests choose to join, every message includes an opt-out, and offers like a free appetizer or birthday dessert are messages people actually want."),
            ("How many texts should a restaurant send?", "Most restaurants do well with the automated messages plus two to four promotional texts a month. More than about one a week tends to increase opt-outs."),
            ("Does it work for counter-service and cafés, not just sit-down restaurants?", "Yes. Cafés, taquerias, pizza shops, and quick-service spots with frequent, lower-ticket visits are often the best fit, because a punch card and bounce-back offer change habits quickly."),
        ],
    },
    {
        "path": "salons/",
        "kind": "industry",
        "nav": "Salons & Spas",
        "title": "Text Loyalty Programs for Salons & Spas in San Diego | Loyalty Program Guy",
        "h1": "Text Message Loyalty Programs for Salons and Spas",
        "description": "How salons, barbershops, and spas use automated text loyalty programs to rebook clients, fill last-minute openings, and grow reviews. Local setup in San Diego County.",
        "answer": "For a salon or spa, a text loyalty program keeps clients on a regular schedule. It reminds them when they're due, rewards them for coming back, fills last-minute openings with a quick text, and asks happy clients for reviews, all automatically.",
        "body": """
<h2>The real problem: clients drifting</h2>
<p>A client who should come in every six weeks slips to nine, then books somewhere else. Nothing went wrong; nobody reminded them. A text program closes that gap by reaching out right when a client is due, with a small reason to book now.</p>

<h2>What the program does for a salon or spa</h2>
<ul>
  <li><strong>“Time for your next visit” texts:</strong> sent after the number of days you choose since their last check-in.</li>
  <li><strong>Last-minute openings:</strong> a cancellation at 2 p.m. becomes a text to your list and a filled chair.</li>
  <li><strong>Digital punch card:</strong> reward every fifth or tenth service.</li>
  <li><strong>Birthday rewards:</strong> a treatment upgrade or product discount during their birthday month.</li>
  <li><strong>Review requests:</strong> happy clients get a direct link to your review page after a repeat visit.</li>
  <li><strong>Product and service launches:</strong> tell regulars first about new treatments or retail products.</li>
</ul>

<h2>Run the numbers for a salon</h2>
<div class="example">
  <p>Example: 300 clients × $65 average ticket × one extra visit every four months (0.25 per month)</p>
  <p class="big">≈ $4,875 more per month</p>
  <p class="note">An illustration, not a promise. Results depend on your client list, offers, and staff participation. <a href="/card/">Try your own numbers</a>.</p>
</div>

<h2>Offers that fit salons and spas</h2>
<ul>
  <li>$10 off a service booked within 7 days of a “you're due” text.</li>
  <li>A free add-on (deep conditioning, brow wax, hot towel) on the fifth visit.</li>
  <li>Refer-a-friend rewards for both clients.</li>
</ul>
<p>Discounts don't have to be big. For salons, a well-timed reminder often does more than the discount itself.</p>

<h2>How setup works</h2>
<p>I set up the kiosk and signs at your front desk, build the campaigns around your booking cycle, and train your team on inviting clients at checkout. Then we review results together each month. See <a href="/guides/how-to-get-repeat-customers/">how to get more repeat customers</a>.</p>
""",
        "faqs": [
            ("Does this replace my booking software?", "No. It works alongside it. Your booking system handles appointments; the loyalty program handles reminders, rewards, openings, and reviews for clients who opted in."),
            ("Is it worth it for a small salon or a single barber?", "Often, yes. A small shop with a loyal client base can see a meaningful lift from filling a few extra appointments a week. Run your numbers first to see if it makes sense."),
            ("Can I text clients about openings the same day?", "Yes. You can send a custom text anytime, which makes it easy to fill a cancellation within hours."),
        ],
    },
    {
        "path": "retail/",
        "kind": "industry",
        "nav": "Retail",
        "title": "Text Loyalty Programs for Retail Shops in San Diego | Loyalty Program Guy",
        "h1": "Text Message Loyalty Programs for Retail Shops",
        "description": "How local retail shops use automated text loyalty programs to drive foot traffic, move inventory, and compete with online stores. Local setup in San Diego County.",
        "answer": "For a retail shop, a text loyalty program turns one-time shoppers into regulars. Customers check in at the counter, earn rewards, and get texts about new arrivals, flash sales, and VIP events, giving them a reason to visit your store instead of ordering online.",
        "body": """
<h2>How local shops compete with online stores</h2>
<p>Online retailers email your customers every week. A local shop can do better with a short, personal text: “New arrivals just came in, and members get 15% off this weekend.” Texts are read quickly and feel personal, which is exactly what a neighborhood store has over a website.</p>

<h2>What the program does for a retail shop</h2>
<ul>
  <li><strong>Flash sales:</strong> clear seasonal inventory with a same-day text.</li>
  <li><strong>New arrival alerts:</strong> let your best customers shop first.</li>
  <li><strong>Digital punch card:</strong> reward frequent shoppers without paper cards.</li>
  <li><strong>“We miss you” offers:</strong> bring back shoppers who haven't visited in a while.</li>
  <li><strong>Events:</strong> fill in-store events, trunk shows, and holiday shopping nights.</li>
  <li><strong>Review requests:</strong> collect reviews that help new shoppers find you.</li>
</ul>

<h2>Run the numbers for a retail shop</h2>
<div class="example">
  <p>Example: 600 customers × $45 average ticket × half an extra visit per month</p>
  <p class="big">≈ $13,500 more per month</p>
  <p class="note">An illustration, not a promise. Results depend on your list, offers, and staff participation. <a href="/card/">Try your own numbers</a>.</p>
</div>

<h2>Offers that fit retail</h2>
<ul>
  <li>Members-only early access to sales.</li>
  <li>A reward after a set amount spent or number of visits.</li>
  <li>Birthday month discounts.</li>
  <li>Double points during slow weeks.</li>
</ul>

<h2>How setup works</h2>
<p>I install the kiosk and counter signs in person, set up your campaigns, and train staff to invite shoppers at checkout. We review results every month. Compare <a href="/guides/punch-card-vs-text-loyalty-program/">paper punch cards vs. a text program</a>.</p>
""",
        "faqs": [
            ("What kinds of retail stores does this work for?", "Stores with customers who can visit more than a few times a year: boutiques, gift shops, pet stores, nutrition and vape shops, bike shops, garden centers, and similar local businesses."),
            ("Can I send different offers to different customers?", "Yes. Automated messages are triggered by each customer's own activity, like a birthday or time since their last visit, and you can also send custom texts anytime."),
            ("Do customers need to download an app?", "No. Customers join with their phone number and receive regular texts. There's no app and no card to carry."),
        ],
    },
    # ---------------------------------------------------------------- guides
    {
        "path": "guides/how-to-get-repeat-customers/",
        "kind": "guide",
        "nav": "How to get repeat customers",
        "title": "How to Get More Repeat Customers: 9 Ways for Local Businesses",
        "h1": "How to Get More Repeat Customers (9 Ways That Work for Local Businesses)",
        "description": "Practical ways restaurants, salons, and shops can get customers to come back: capture contact info, reward the second visit, win back lapsed customers, and more.",
        "answer": "To get more repeat customers, capture every customer's contact information with their permission, give them a reason to come back soon after the first visit, reward frequent visits, reach out automatically when someone stops coming in, and make each visit personal. The key is doing this consistently, which is why most businesses automate it.",
        "body": """
<h2>1. Capture contact information on the first visit</h2>
<p>You can't bring someone back if you can't reach them. The biggest mistake local businesses make is letting first-time customers leave anonymously. Ask every customer to join a rewards list with their phone number, and give them a small reason to say yes.</p>

<h2>2. Reward the second visit, fast</h2>
<p>The second visit is the hardest one to earn and the most valuable. A bounce-back offer, like a discount on a return visit within 14 or 30 days, turns a single visit into the start of a habit.</p>

<h2>3. Make progress visible</h2>
<p>A punch card works because customers can see themselves getting closer to a reward. A digital punch card does the same thing without lost cards.</p>

<h2>4. Win back customers who stop coming</h2>
<p>Most customers don't leave because of a bad experience; they drift. An automatic “we miss you” message after 30, 60, or 90 days without a visit brings many of them back. See <a href="/guides/win-back-text-examples/">win-back text examples</a>.</p>

<h2>5. Recognize birthdays and anniversaries</h2>
<p>A personal offer on a customer's birthday or the anniversary of joining gives them a natural reason to visit and makes them feel remembered.</p>

<h2>6. Use slow periods on purpose</h2>
<p>Send offers when you have capacity: a slow Tuesday, a rainy afternoon, an open appointment slot. Filling empty capacity is almost pure profit.</p>

<h2>7. Ask repeat customers for reviews</h2>
<p>Customers who come back are your happiest ones. Ask them for a review after their second or third visit, and new customers will find you more easily.</p>

<h2>8. Train staff to invite every customer</h2>
<p>A loyalty program only grows if staff mention it every time. A simple script at checkout (“Want to join our rewards? You'll get $5 off your next visit”) makes a bigger difference than any sign.</p>

<h2>9. Track return visits, not just sales</h2>
<p>Know how many customers came back this month and how often. If return visits aren't growing, change the offer or the invitation.</p>

<h2>Why retention is worth the effort</h2>
<p>Research published in <em>Harvard Business Review</em> found acquiring a new customer can cost 5 to 25 times more than keeping an existing one, and Bain &amp; Company research found a 5% improvement in retention can raise profits by 25% to 95%. A quick way to see what that means for you is to <a href="/card/">run your own numbers</a>.</p>

<h2>Doing all of this automatically</h2>
<p>Every step above can run on its own with a text message loyalty program: customers join at a kiosk, and bounce-back offers, punch cards, win-back messages, birthday rewards, and review requests send automatically. That's what I set up for businesses in San Diego County. See how it works for <a href="/restaurants/">restaurants</a>, <a href="/salons/">salons and spas</a>, and <a href="/retail/">retail shops</a>.</p>
""",
        "faqs": [
            ("What is the most effective way to get repeat customers?", "Capturing contact information with permission and following up automatically. Without a way to reach customers after they leave, every other tactic depends on hoping they remember you."),
            ("How soon should you follow up with a new customer?", "Within the first few days, while the experience is fresh. A bounce-back offer that expires in 14 to 30 days works well for most local businesses."),
            ("Are text messages or emails better for bringing customers back?", "For local businesses, texts usually get noticed faster and feel more personal. Email still works for longer content. Many businesses use texts for offers and reminders."),
        ],
    },
    {
        "path": "guides/punch-card-vs-text-loyalty-program/",
        "kind": "guide",
        "nav": "Punch card vs. text loyalty",
        "title": "Punch Card vs. Text Message Loyalty Program: Which Is Better?",
        "h1": "Paper Punch Card vs. Text Message Loyalty Program",
        "description": "A side-by-side comparison of paper punch cards and text message loyalty programs for local businesses: cost, customer data, follow-up, fraud, and results.",
        "answer": "A paper punch card is cheap and simple, but you never learn who your customers are and you can't reach them after they leave. A text message loyalty program costs more, but it captures each customer's number with permission, rewards visits automatically, and lets you bring customers back with offers and reminders.",
        "body": """
<h2>Side-by-side comparison</h2>
<div class="table-wrap">
<table>
  <tr><th></th><th>Paper punch card</th><th>Text loyalty program</th></tr>
  <tr><td><strong>Upfront cost</strong></td><td>Very low (printing)</td><td>Monthly subscription plus setup</td></tr>
  <tr><td><strong>Know who your customers are</strong></td><td>No</td><td>Yes, with their permission</td></tr>
  <tr><td><strong>Reach customers after they leave</strong></td><td>No</td><td>Yes, by text</td></tr>
  <tr><td><strong>Win back customers who stop coming</strong></td><td>No</td><td>Automatic “we miss you” offers</td></tr>
  <tr><td><strong>Birthday rewards</strong></td><td>No</td><td>Automatic</td></tr>
  <tr><td><strong>Lost or forgotten cards</strong></td><td>Common</td><td>Not an issue; it's their phone number</td></tr>
  <tr><td><strong>Fake stamps and fraud</strong></td><td>Possible</td><td>Visits are recorded at check-in</td></tr>
  <tr><td><strong>Track results</strong></td><td>Guesswork</td><td>Visit and return-rate reports</td></tr>
  <tr><td><strong>Staff effort</strong></td><td>Stamp every visit</td><td>Invite customers to join; the rest is automatic</td></tr>
</table>
</div>

<h2>When a paper punch card is enough</h2>
<p>If you're just starting out, have very few repeat customers, or can't commit a small monthly budget, a punch card is better than nothing. It still rewards repeat visits.</p>

<h2>When a text program pays for itself</h2>
<p>If you have a steady flow of customers who could visit more often, the ability to reach them is what makes the difference. A punch card only works when the customer is already standing at your counter. A text program works when they're at home deciding where to eat, shop, or book.</p>
<p>A simple test: estimate how many customers you see in a month and your average ticket, then <a href="/card/">see what one extra visit is worth</a>. Compare that with <a href="/guides/sms-loyalty-program-cost/">what a text program costs</a>.</p>

<h2>Switching from punch cards</h2>
<p>You don't have to cut off existing punch card holders. Most businesses honor existing cards and invite those customers to join the text program, often with a bonus visit credited for switching.</p>
""",
        "faqs": [
            ("Do customers still like punch cards?", "Many do, because they're simple. A digital punch card keeps that same visible progress toward a reward, without a card to carry or lose."),
            ("Is a text loyalty program hard for older customers?", "Usually not. Joining takes a phone number and a tap on a kiosk, and rewards arrive as ordinary text messages. No app is required."),
            ("Can I use both?", "Yes, especially during a switch. Over time most businesses move fully to the text program because it does everything the card does, plus follow-up."),
        ],
    },
    {
        "path": "guides/sms-loyalty-program-cost/",
        "kind": "guide",
        "nav": "What does it cost?",
        "title": "How Much Does an SMS Loyalty Program Cost? (2026 Pricing Guide)",
        "h1": "How Much Does an SMS Loyalty Program Cost?",
        "description": "What a text message loyalty program costs for a small business: monthly plans, setup fees, message overages, compliance fees, and how to tell if it will pay for itself.",
        "answer": "Most SMS loyalty programs for local businesses cost roughly $99 to $400 per month, depending on how many texts are included and whether a check-in kiosk is part of the plan, plus a one-time setup fee. Watch for message overage charges, annual compliance fees, and contract length when comparing options.",
        "body": """
<h2>What you're paying for</h2>
<ul>
  <li><strong>Monthly plan:</strong> the software, a set number of included texts, and support.</li>
  <li><strong>Check-in kiosk:</strong> a tablet at your counter where customers join and check in. Plans with a kiosk cost more but grow your list much faster.</li>
  <li><strong>Setup or launch fee:</strong> one-time installation, campaign setup, signage, and staff training.</li>
  <li><strong>Carrier registration:</strong> business texting now requires registering with phone carriers. Good providers handle this for you.</li>
  <li><strong>Extra messages:</strong> texts beyond your plan are billed per message.</li>
  <li><strong>Compliance fees:</strong> some providers charge an annual fee to cover carrier and regulatory requirements.</li>
</ul>

<h2>The plans I offer</h2>
<p>I'm a local agent for SenText Solutions' Repeat Business Program. Current plans:</p>
<div class="table-wrap">
<table>
  <tr><th>Plan</th><th>Monthly</th><th>Texts included</th><th>Kiosk</th></tr>
  <tr><td>Starter</td><td>$99</td><td>500</td><td>No</td></tr>
  <tr><td>Essential</td><td>$199</td><td>1,000</td><td>Yes</td></tr>
  <tr><td>Growth</td><td>$299</td><td>1,500</td><td>Yes</td></tr>
  <tr><td>Premier</td><td>$399</td><td>2,000</td><td>Yes</td></tr>
</table>
</div>
<p>Every plan also includes installation and staff training, carrier approval and registration, campaign support, and free opt-in signage (banner, counter signs, digital sign, social graphic, and staff buttons).</p>
<p><strong>Other costs to know up front:</strong> a one-time launch fee (quoted in your walkthrough), a $99 annual compliance fee billed each December, and $0.079 per text beyond your plan. Agreements are 12 months and renew automatically unless cancelled in writing at least 30 days before renewal.</p>
<p class="note">Pricing current as of September 2026 and set by SenText Solutions; subject to change.</p>

<h2>Will it pay for itself?</h2>
<p>Add up a year of cost, then compare it with the revenue from extra visits. For example, a $299 plan for 12 months plus the $99 compliance fee is $3,687 before the launch fee. At a $25 average ticket, that's about 148 extra visits over a year, or roughly 12 a month, to break even.</p>
<p>That's why I back programs with a <a href="/#guarantee">3x ROI Guarantee</a>: if the program doesn't return at least three times what you invested in the first 12 months, SMB AI Partners pays your monthly service until it does. Terms apply. <a href="/card/">Run your own numbers</a>.</p>

<h2>Questions to ask any provider</h2>
<ul>
  <li>How many texts are included, and what does each extra text cost?</li>
  <li>Is there a setup fee, and what does it include?</li>
  <li>How long is the contract, does it auto-renew, and how do I cancel?</li>
  <li>Are there annual or compliance fees?</li>
  <li>Who handles carrier registration and opt-out compliance?</li>
  <li>Who trains my staff, and who do I call when I need help?</li>
</ul>
""",
        "faqs": [
            ("Is there a cheaper option than a monthly SMS program?", "A paper punch card costs almost nothing, but it can't reach customers after they leave. See the punch card vs. text program comparison to decide which fits your business."),
            ("Why do plans with a kiosk cost more?", "The kiosk includes hardware and makes joining effortless at your counter, which usually grows your customer list much faster than signs alone."),
            ("Can I cancel anytime?", "With the plans I offer, agreements are 12 months and auto-renew unless cancelled in writing at least 30 days before renewal. Always check contract terms before signing with any provider."),
        ],
    },
    {
        "path": "guides/win-back-text-examples/",
        "kind": "guide",
        "nav": "Win-back text examples",
        "title": "Win-Back Text Message Examples for Restaurants, Salons & Shops",
        "h1": "Win-Back Text Message Examples That Bring Customers Back",
        "description": "Copy-and-paste win-back text message examples for restaurants, salons, and retail shops, plus when to send them and the rules to follow.",
        "answer": "A good win-back text is short, personal, and gives a clear reason to return with a deadline, like “We miss you, Sam! Here's $5 off your next visit, good through Sunday.” Send it after a customer goes longer than usual without visiting, and always include a way to opt out.",
        "body": """
<h2>When to send a win-back text</h2>
<p>Base the timing on how often a typical customer visits:</p>
<ul>
  <li><strong>Coffee shops and quick-service:</strong> 14 to 30 days without a visit.</li>
  <li><strong>Restaurants:</strong> 30 to 60 days.</li>
  <li><strong>Salons and barbers:</strong> 2 to 4 weeks past their usual rebooking time.</li>
  <li><strong>Retail:</strong> 60 to 90 days.</li>
</ul>
<p>A second, slightly stronger offer 30 days after the first can recover customers who ignored the first message.</p>

<h2>Restaurant examples</h2>
<p class="sms">Hi Dana, it's been a while! Come back this week and your first drink is on us. Show this text by Sunday. Reply STOP to opt out.</p>
<p class="sms">We miss you at Marco's! Here's 15% off your next order, good through Friday. Reply STOP to opt out.</p>

<h2>Salon and spa examples</h2>
<p class="sms">Hi Jess, you're due for a refresh! Book in the next 7 days and get a free deep conditioning treatment. Reply STOP to opt out.</p>
<p class="sms">We have openings Thursday afternoon and saved one for you: $10 off any service booked this week. Reply STOP to opt out.</p>

<h2>Retail examples</h2>
<p class="sms">Hi Chris, new arrivals just landed and we thought of you. Stop by this weekend for 20% off one item. Reply STOP to opt out.</p>
<p class="sms">It's been a while! Your $10 reward is waiting, good through the end of the month. Reply STOP to opt out.</p>

<h2>What makes a win-back text work</h2>
<ul>
  <li><strong>Use their first name.</strong> It reads as a personal note, not an ad.</li>
  <li><strong>One clear offer.</strong> Don't list three deals.</li>
  <li><strong>A deadline.</strong> “Good through Sunday” creates a reason to act now.</li>
  <li><strong>Short.</strong> One or two sentences.</li>
  <li><strong>Your business name</strong> so they know who it's from.</li>
</ul>

<h2>Rules to follow</h2>
<ul>
  <li>Only text customers who opted in to receive marketing messages from you.</li>
  <li>Include a way to opt out, such as “Reply STOP to opt out,” and honor it.</li>
  <li>Send at reasonable hours, generally between 8 a.m. and 9 p.m. in the customer's time zone.</li>
  <li>Avoid public link shorteners; carriers may filter them.</li>
</ul>
<p class="note">General information, not legal advice. Texting rules are set by the TCPA, carriers, and state laws.</p>

<h2>Sending these automatically</h2>
<p>With a text loyalty program, win-back messages send on their own the moment a customer passes the number of days you choose, then reset when they check in again. Learn more about <a href="/guides/how-to-get-repeat-customers/">getting more repeat customers</a>.</p>
""",
        "faqs": [
            ("How big should a win-back discount be?", "Usually smaller than people expect. A free drink, a small add-on, or $5 to $10 off is often enough, because the reminder does most of the work."),
            ("How many win-back texts should I send?", "One or two per lapse is plenty: a first message, then a slightly stronger offer about 30 days later if they still haven't returned."),
            ("Do win-back texts annoy customers?", "Not when customers opted in, the message is relevant, and they can opt out easily. Customers who don't want messages can reply STOP."),
        ],
    },
    # ---------------------------------------------------------------- about
    {
        "path": "about/",
        "kind": "about",
        "nav": "About",
        "title": "About Kevin Graham, the Loyalty Program Guy | San Diego County",
        "h1": "Hi, I'm Kevin Graham",
        "description": "Kevin Graham, founder of SMB AI Partners in Poway, CA, helps San Diego County restaurants, salons, and retail shops get more repeat customers with text loyalty programs.",
        "answer": "",
        "body": """
<div class="about-hero">
  <img src="/images/kevin-graham-headshot.jpg" alt="Kevin Graham, founder of SMB AI Partners" width="800" height="1096">
  <div>
    <p class="lede">I help local restaurants, salons, and retail shops across San Diego County get more repeat customers.</p>
    <p>I'm the founder of SMB AI Partners, based in Poway, California, and a local agent for SenText Solutions' Repeat Business Program. I started SMB AI Partners because the tools that help big companies keep customers coming back should be available to local businesses too.</p>
  </div>
</div>

<h2>What I do</h2>
<p>Most small businesses work hard to win a first visit, then have no system to earn the next one. I set up automated text message loyalty programs that fix that: a check-in kiosk, signage, and campaigns that bring customers back with bounce-back offers, digital punch cards, birthday rewards, win-back messages, and review requests.</p>

<h2>How I work</h2>
<ul>
  <li><strong>Local, in person.</strong> I install your kiosk and signs myself and train your staff.</li>
  <li><strong>I stay involved.</strong> We review your numbers together every month. If participation dips, I bring you a fix.</li>
  <li><strong>One point of contact.</strong> You work with me, not a call center.</li>
  <li><strong>Accountable for results.</strong> Programs are backed by the SMB AI Partners <a href="/#guarantee">3x ROI Guarantee</a>.</li>
</ul>

<h2>Background</h2>
<p>My background is in B2B sales and territory management, with graduate study in marketing analytics. That combination is what I bring to every client: practical, local service, and a focus on what the numbers actually say.</p>

<h2>Where I work</h2>
<p>San Diego County, including Poway, San Diego, Escondido, Rancho Bernardo, Ramona, Carlsbad, and surrounding communities.</p>

<h2>Learn more</h2>
<div class="cards">
  <a href="/restaurants/"><strong>Restaurants</strong>Fill slow nights and bring diners back.</a>
  <a href="/salons/"><strong>Salons &amp; spas</strong>Keep clients on schedule.</a>
  <a href="/retail/"><strong>Retail shops</strong>Drive foot traffic and move inventory.</a>
  <a href="/guides/"><strong>Guides</strong>Practical advice on repeat customers.</a>
</div>
""",
        "faqs": [],
    },
]

GUIDES = [p for p in PAGES if p["kind"] == "guide"]
INDUSTRIES = [p for p in PAGES if p["kind"] == "industry"]


def header():
    return f"""<header class="site-header"><div class="inner">
  <a class="brand" href="/"><img src="/images/smb-ai-partners-logo-header.png" width="380" height="250" alt="SMB AI Partners logo">Loyalty Program Guy</a>
  <nav class="site-nav" aria-label="Main">
    <a href="/restaurants/">Restaurants</a><a href="/salons/">Salons</a><a href="/retail/">Retail</a>
    <a href="/guides/">Guides</a><a href="/about/">About</a>
    <a class="btn-sm" href="{CALENDLY}" data-cta="nav_book">Book a demo</a>
  </nav>
</div></header>"""


def footer():
    ind = "".join(f'<a href="/{p["path"]}">{escape(p["nav"])}</a><br>' for p in INDUSTRIES)
    gd = "".join(f'<a href="/{p["path"]}">{escape(p["nav"])}</a><br>' for p in GUIDES)
    return f"""<footer class="site-footer"><div class="inner">
  <div><strong>Loyalty Program Guy</strong>Powered by SMB AI Partners<br>Serving San Diego County, CA<br>
    <a href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><br><a href="mailto:kevin@smbaipartners.com">kevin@smbaipartners.com</a></div>
  <div><strong>Industries</strong>{ind}</div>
  <div><strong>Guides</strong>{gd}<a href="/card/">Repeat-visit calculator</a></div>
  <div><strong>Company</strong><a href="/">Home</a><br><a href="/about/">About Kevin</a><br><a href="/#guarantee">3x ROI Guarantee</a><br><a href="https://www.smbaipartners.com/">SMB AI Partners</a><br>
    <span>© <span class="yr">{date.today().year}</span></span></div>
</div></footer>"""


def cta():
    return f"""<section class="cta">
  <h2>See what this could do for your business</h2>
  <p>Free 15-minute walkthrough. I'll run your numbers with you.</p>
  <div class="buttons">
    <a class="primary" href="{CALENDLY}" data-cta="book">Book a free walkthrough</a>
    <a class="secondary" href="sms:{PHONE_E164}?&body=Hi%20Kevin%2C%20I%20found%20your%20site.%20My%20business%20is%3A%20" data-cta="text">Text Kevin: {PHONE_DISPLAY}</a>
  </div>
  <p class="fine">Backed by our <a href="/#guarantee">3x ROI Guarantee</a>. Terms apply.</p>
</section>"""


def faq_html(faqs):
    if not faqs:
        return ""
    items = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faqs)
    return f'<section class="faq"><h2>Frequently asked questions</h2>{items}</section>'


def schema(page, url, crumbs):
    graph = [{
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)],
    }]
    if page["kind"] == "guide":
        graph.append({
            "@type": "Article", "headline": page["h1"], "description": page["description"],
            "author": {"@id": PERSON["@id"]}, "publisher": {"@type": "Organization", "name": "SMB AI Partners"},
            "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": url,
            "image": f"{SITE}/images/kevin-graham-headshot.jpg",
        })
    elif page["kind"] == "industry":
        graph.append({
            "@type": "Service", "name": page["h1"], "description": page["description"], "url": url,
            "serviceType": "Customer loyalty program setup and management",
            "areaServed": {"@type": "AdministrativeArea", "name": "San Diego County, CA"},
            "provider": {"@type": "Organization", "name": "SMB AI Partners", "url": SITE + "/", "telephone": "+1-858-218-6905", "founder": {"@id": PERSON["@id"]}},
        })
    elif page["kind"] == "about":
        graph.append({"@type": "ProfilePage", "url": url, "mainEntity": {
            **PERSON, "address": {"@type": "PostalAddress", "addressLocality": "Poway", "addressRegion": "CA", "addressCountry": "US"},
            "knowsAbout": ["customer loyalty programs", "SMS marketing", "customer retention", "repeat customers", "small business marketing"]}})
    if page["kind"] != "about":
        graph.append(PERSON)
    if page["faqs"]:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faqs"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def render(page, crumbs, body_html, answer_html=""):
    url = f"{SITE}/{page['path']}"
    crumb_html = " › ".join(f'<a href="{u}">{escape(n)}</a>' for n, u in crumbs[:-1]) + f" › {escape(crumbs[-1][0])}"
    byline = ""
    if page["kind"] == "guide":
        byline = '<div class="byline"><img src="/images/kevin-graham-headshot.jpg" alt="" width="36" height="36"><span>By <a href="/about/">Kevin Graham</a> · Updated ' + date.today().strftime("%B %Y") + "</span></div>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(page['title'])}</title>
  <meta name="description" content="{escape(page['description'])}" />
  <link rel="canonical" href="{url}" />
  <meta property="og:title" content="{escape(page['title'])}" />
  <meta property="og:description" content="{escape(page['description'])}" />
  <meta property="og:type" content="{'article' if page['kind'] == 'guide' else 'website'}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/images/kevin-graham-headshot.jpg" />
  <link rel="icon" href="/favicon.ico" sizes="32x32" />
  <link rel="apple-touch-icon" href="/images/apple-touch-icon.png" />
  <meta name="theme-color" content="#1e3a8a" />
  <link rel="stylesheet" href="/css/pages.css" />
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  <script type="application/ld+json">
{schema(page, url, crumbs)}
  </script>
</head>
<body>
{header()}
<nav class="crumbs" aria-label="Breadcrumb">{crumb_html}</nav>
<article>
  <h1>{escape(page['h1'])}</h1>
  {byline}
  {answer_html}
  {body_html}
  {faq_html(page['faqs'])}
  {cta()}
</article>
{footer()}
<script>
  document.querySelectorAll('[data-cta]').forEach(a => a.addEventListener('click', () => {{
    if (typeof gtag === 'function') gtag('event', 'generate_lead', {{ method: a.dataset.cta, page: location.pathname }});
  }}));
</script>
</body>
</html>
"""


def write(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    for p in PAGES:
        if p["kind"] == "guide":
            crumbs = [("Home", "/"), ("Guides", "/guides/"), (p["nav"], "/" + p["path"])]
        else:
            crumbs = [("Home", "/"), (p["nav"], "/" + p["path"])]
        answer = f'<div class="answer"><p><strong>Short answer:</strong> {escape(p["answer"])}</p></div>' if p["answer"] else ""
        write(os.path.join(p["path"], "index.html"), render(p, crumbs, p["body"], answer))

    # Guides index
    cards = "".join(f'<a href="/{g["path"]}"><strong>{escape(g["h1"])}</strong>{escape(g["description"])}</a>' for g in GUIDES)
    ind_cards = "".join(f'<a href="/{p["path"]}"><strong>{escape(p["nav"])}</strong>{escape(p["description"])}</a>' for p in INDUSTRIES)
    idx = {"path": "guides/", "kind": "index", "nav": "Guides", "faqs": [],
           "title": "Guides: Getting More Repeat Customers | Loyalty Program Guy",
           "h1": "Guides for Getting More Repeat Customers",
           "description": "Practical guides for local business owners on repeat customers, loyalty programs, win-back texts, and what text loyalty programs cost."}
    body = f'<p class="lede">Straightforward advice for restaurants, salons, and retail shops that want customers to come back more often.</p><div class="cards">{cards}</div><h2>By industry</h2><div class="cards">{ind_cards}</div><p><a href="/card/">Try the repeat-visit calculator</a></p>'
    write("guides/index.html", render(idx, [("Home", "/"), ("Guides", "/guides/")], body))

    # sitemap.xml
    urls = ["", "card/"] + [p["path"] for p in PAGES] + ["guides/"]
    items = "".join(f"  <url>\n    <loc>{SITE}/{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n')

    # llms.txt (https://llmstxt.org)
    lines = [
        "# Loyalty Program Guy",
        "",
        "> Kevin Graham (SMB AI Partners, Poway, CA) sets up and manages automated text message loyalty programs that help restaurants, salons, spas, and retail shops in San Diego County get more repeat customers. Local SenText Solutions agent. Programs are backed by the SMB AI Partners 3x ROI Guarantee.",
        "",
        f"Contact: text or call {PHONE_DISPLAY}, kevin@smbaipartners.com, or book a free walkthrough at {CALENDLY}.",
        "",
        "## Services by industry",
    ]
    lines += [f"- [{p['h1']}]({SITE}/{p['path']}): {p['description']}" for p in INDUSTRIES]
    lines += ["", "## Guides"]
    lines += [f"- [{g['h1']}]({SITE}/{g['path']}): {g['description']}" for g in GUIDES]
    lines += ["", "## About",
              f"- [About Kevin Graham]({SITE}/about/): background, service area, and how he works with clients.",
              f"- [Home and 3x ROI Guarantee]({SITE}/): overview of the program, process, FAQ, and guarantee.",
              f"- [Repeat-visit calculator]({SITE}/card/): estimate added monthly revenue from one extra visit per customer.", ""]
    write("llms.txt", "\n".join(lines))
    print(f"built {len(PAGES) + 1} pages, sitemap ({len(urls)} urls), llms.txt")


if __name__ == "__main__":
    main()
