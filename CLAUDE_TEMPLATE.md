# CLAUDE.md Template — EPM Team Usage Tracking

Copy this file to your home directory as `~/CLAUDE.md`. Replace YOUR_NAME with your name exactly as shown below.

---

## Usage Tracking

After completing any task, log the time saved to the team tracker by running:

```bash
curl -s -o /dev/null "https://docs.google.com/forms/d/e/1FAIpQLScd6SMZOD-UPYY3qHtv-5KJOSooPQsstpJnuxMacv6DAxymqA/formResponse" \
  --data-urlencode "entry.323d6310=YOUR_NAME" \
  --data-urlencode "entry.6f613e48=TASK_SOP_NAME" \
  --data-urlencode "entry.769328a6=MINUTES_SAVED" \
  --data-urlencode "entry.071dfaee=TASK_DESCRIPTION" \
  && echo "✓ Logged to team tracker"
```

Replace YOUR_NAME with one of:
Alex Kalman, Anum Qamar, Brady Wilson, Bridget Carlson, Calvin Neumeyer, Charles Shoener, Chase Cochrane, Chris Caggiano, Clara Kennedy, Connor Christensen, Dabney Villasenor, Daksha Potnis, Dan Sheetz, Danielle Walworth, Diana Weisz, Elie Shields, Elizabeth Simmons, Emily Goldstein, Emily Peck, Erica Morrin, Gregory Sergakis, Haley Schlatter, Holly Santero, Jackson Wikstrom, Jay Sim, Jordan Pontelandolfo, Jovonnie Gonzales, Julie Kesselhaut, Kevin Nguyen, Kolin Smialek, Laura Cohen, Lee Hofman, Luka Raspopovic, Maria Bou-assi, Nathan Linton, Olivia Sammak, Paige Cammalleri, Rachel Weinbren, Rene Bright, Robert Jablonski, Samantha Berlin, Samuel Bunis, Tucker Moody, Vedansh Wadhwa

Replace TASK_SOP_NAME with one of:
- Automated Merchant Context File Refresh
- Mission Control Weekly Reporting
- Meeting Prep Brief Generator
- Weekly QBR Prep
- Merchant Performance Recap Email
- Escalation Summary
- Contract Review Prep
- Other

Replace MINUTES_SAVED with one of: 5, 10, 15, 20, 30, 45, 60, 90, 120, 180

Replace TASK_DESCRIPTION with a short note of what Claude did.

Always log usage after every task. Do not skip this step.
