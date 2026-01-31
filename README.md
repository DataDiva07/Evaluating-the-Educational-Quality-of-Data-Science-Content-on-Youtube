#  Evaluating Educational Quality of Data Science Content on YouTube
This project analyzes the educational quality of Data Science videos on YouTube using sentiment analysis, transcript evaluation, and unsupervised clustering. Instead of relying on popularity metrics such as views or subscribers, the focus is on instructional depth, clarity, and learner perception.

##  Project Objective

- Evaluate educational quality beyond popularity metrics  

- Analyze learner sentiment from YouTube comments  

- Assess instructional quality using video transcripts  

- Study the influence of instructor background on content quality  
---

##  Data Sources
- YouTube Data API (views, likes, comments, channel metadata)  

- YouTube Transcript API (video transcripts)  

- Google Scholar (h-index and citation data for scientist instructors)  
---

##  Methodology

- <b>Data Cleaning \& Preprocessing:</b> Text normalization, noise removal, feature engineering  

- <b> Sentiment Analysis:</b> Fine-tuned RoBERTa model to classify comments as positive, neutral, or negative  

- <b>Transcript Analysis:</b> Scoring videos on technical depth, clarity, structure, engagement, and practical value  

- <b> Clustering:</b> K-Means and DBSCAN applied to sentiment and transcript features  

- <b> Instructor Analysis:</b> Role-based interpretation (scientist, employee, freelancer)  
---

##  Content Clusters Identified

1\. High-Technical \& Structured Content  

2\. Beginner-Friendly \& Positive Content  

3\. Dense, Negative-Sentiment Content  

4\. Low-Technical, Emotion-Driven Content  

---

##  Key Insights

- High engagement does not necessarily indicate high educational quality  

- Beginner-friendly and emotion-driven content receives higher interaction  

- High-technical content provides stable learning value  

- Scientist instructors dominate technically strong content  
---
##  Conclusion

Educational quality on YouTube cannot be judged using popularity metrics alone.  

By combining learner sentiment, transcript analysis, and instructor background, this project provides a data-driven approach to evaluating the true educational value of Data Science content.

