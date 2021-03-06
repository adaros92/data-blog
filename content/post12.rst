**************************
Tech Interviews Are Broken
**************************

:date: 2021-01-18 00:00
:modified: 2021-01-18 00:00
:tags: Career
:category: Career
:authors: Adams Rosales
:summary: Do you even LeetCode bro?
:header_cover: /static/post12/header.jpg

Exhibit A
#########
Did you know that there are companies out there dedicated to nothing more than helping you prepare to pass a tech
interview? Below are some of the ones I've heard of recently.

- `Interview Kickstart  <https://www.interviewkickstart.com/guide/interview-kickstart-cost/>`_
- `Outco <https://www.outco.io/>`_
- `AlgoExpert <https://www.algoexpert.io/purchase>`_

Look I understand that data structures and algorithms are an important foundation to any job that requires serious
system design and development. I am a huge advocate for truly understanding the concepts at their core rather than
focusing on the superficial surface-level frameworks and such. However, there has to be something wrong with your process
when there is a whole industry dedicated to helping people answer your interview questions.

Tech companies are signaling that being able to answer coding puzzles that require you to spend weeks to months reading
interview prep books and spending thousands of dollars on classes from the institutions above is more important than
actually being a good developer. I say this as both someone who has been rejected from roles that I would have been able to
add value in and who has interviewed candidates for tech roles at big tech but had to turn them down despite
their valuable levels of experience.

LeetCode trumps experience every time. You could have literally created an application that is used by most of the people
in the prospective company. It doesn't matter if you can't also reverse a linked list from muscle memory. Case and point
with this Tweet by the creator of Homebrew.

.. image:: /static/post12/post12_homebrew.png
  :width: 100%
  :alt: Max Howell on Google's interviewing methodology

So Should We Just Suck It Up?
#############################
While it's relatively easy to spend a few weeks or months reviewing old concepts you never have to implement from
scratch on the job like binary trees, heaps, tries, etc. I think it adds absolutely no value whatsoever and it detracts
from what's really important. These are my reasons:

**1. A full-time software engineering job should be enough to get another engineering job that requires the same level
of experience**, especially if the person you're interviewing has actual code to demonstrate and designs to walk through.
I don't know about you but I have other shit to do outside of work than prepare for interviews. I could be playing an instrument,
exercising, bonding with my family, walking my dog, hell, even building actual software products just like I would be doing
on the job. All of these are much better uses of my time than reviewing tricky concepts that are hardly ever used in
practice like dynamic programming.

**2. We should incentivize candidates to build solutions to actual real world problems rather than solving toy whiteboard
puzzles.** Imagine if instead of grinding through LeetCode questions to become more cogs in the big tech machine,
all of those talented and passionate kids were building real world applications. I think the industry would be much better
off and there would be more helpful resources out there to judge candidates' talents and experience levels with.

**3. Proponents of the current interviewing system insist that the process measures problem solving skills, but from my
experience the problem solving done on the job is nothing like what is measured by the puzzle-like DS/Algo interview
questions.** The problem solving on the job involves researching new libraries and technologies, dealing with ambiguity,
collaborating with other people, deep diving data to root cause issues, being able to unblock yourself, and managing time
effectively. That's literally 95-99% of what's required. I have never found myself stuck on some mind-bending algorithm
that needs to be implemented right away (and preferably on a whiteboard without referencing any resources). I have never
been stuck on any coding issue unless it's related to not fully understanding how a library or system works. The current
interviews don't measure a candidate's ability to get through those types of problems.

**4. Having a good foundational understanding of algorithms and data structures is not enough to pass whiteboard tech
interview problems.** There is a large "gotcha" component to these questions where simply understanding the foundation
(which data structure to use for what and how to optimize runtime/space complexity given the problem at hand) is not
enough. Given the amount of time that you're allotted to solve those tricky questions it's not possible for most good
engineers to solve them optimally without going through a bunch of similar questions beforehand, including the interviewers
themselves. I know this because I am okay at my job (haven't been fired yet in the 4 or so years of technical
experience under my belt) and I can't consistently solve those tricky questions without extensive review beforehand. The majority of
engineers I work with are also not super geniuses who can take a difficult LeetCode question and solve it on a whiteboard
within 30 minutes without reviewing beforehand. That review requirement is a problem because of reasons 1-3 above.

So no, we should change the process.

A Better Solution
#################
Have the candidates implement a short coding project and write a design doc explaining why they structured it the way they
did and how they would deploy the application and maintain it going forward. Instead of having interviewers give whiteboard
interviews, have them review the code and designs beforehand and ask them relevant questions about it when they speak to
them in person. Ask questions like what metrics they would collect to measure the state of the application, how would
they scale it to X amount of users, how would they troubleshoot a particular issue, etc.

The complexity of these projects and related questions will vary depending on how much experience the candidate has.
Obviously if it's an experienced candidate the interview should mostly focus on previous projects they have worked on.
It's quite easy to tell whether someone knows what they're talking about just by having a technical conversation with them
in person.

The in-person interviews should also involve peer coding questions in a similar environment the candidate would find themselves
in on the job. That means with an IDE and full access to Internet resources, wikis, documentation, etc. If they get stuck
they should be able to look for help online because let's face it, that's one of the most valuable skills a developer could
have. The questions themselves should be relevant to the job. If the job requires the candidate to glue a bunch of API
endpoints together then ask them to do that. If a job requires building a frontend then have them build a frontend UI.
If the job requires writing Spark applications and orchestrating big data jobs then let them show what they got by doing
just that. When they're finished have them explain their code and ask probing questions about how it would be
deployed as part of a scalable system.

It Won't Change Anytime Soon
############################
At least not at big tech companies like FAANG. They just have way too much demand and from their perspective, it's better
to turn away a good candidate that didn't review DS/Algorithms beforehand than bring in a bad candidate who doesn't
actually know what they're doing. That's why they choose to focus on these types of questions. Not so much because they're
good measures of problem solving ability but because they're effective weed-out tools to narrow down the applicant pool
to manageable levels. I understand if we're talking about interviewing fresh college grads who haven't done anything.
It makes absolutely no sense to me when it comes to experienced candidates, but alas that's how it is.

The engineers doing all of the hiring in these companies also tend to give in to industry standards and think it's just
the way it has always been so there's no point in changing. Some even wear their LeetCode ability like
a badge of honor, looking down upon anyone not willing to put in the dedication to solve those questions themselves. It's
quite toxic actually. I've interviewed super qualified candidates before that would have been great assets but my peers
didn't think so because the candidates struggled with esoteric DS questions. I've literally read in the feedback
comments for candidates with years of software experience, "struggled with [insert hard LeetCode question here], not good
at coding," which just boggles my mind. How can you make such a determination from not being able to answer those types of
questions on a whiteboard? Did you even talk to the candidate about their many years of relevant experience and obvious
actual engineering ability?

It's a shame because I think those companies would certainly be better off if their interview process
were more like the actual jobs the candidates need to do once they join. Anyway, hit me up on LeetCode fam -
https://leetcode.com/adaros92/.
