<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
<h1 id="user-based-collaborative-filtering-system">User-Based Collaborative Filtering System</h1>
<p>As the title implies, this project is a user-based collaborative filtering system created for generating predictions for the <a href="https://grouplens.org/datasets/movielens/100k/">Movie Lens</a> 100k dataset originally developed for the <a href="https://grouplens.org/datasets/movielens/100k/">University of Minnesota</a>. The main goals were to: understand the dataset through simple metrics, make efficient predictions, evaluation prediction performance, and run a variety of large scale experiments.</p>

<h2 id="data-observations">Data Observations</h2>
<ul>
  <li>Unique movies: 943</li>
  <li>Unique users: 943</li>
  <li>Average Rating: 3.52986</li>
  <li>Ratings density metric: .112454442</li>
  <li>Total number of…
    <ul>
      <li>1 star ratings: 6110</li>
      <li>2 star ratings: 11,370</li>
      <li>3 star ratings: 27,145</li>
      <li>4 star ratings: 34,174</li>
      <li>5 star ratings: 21,201</li>
      <li>Total: 100,000</li>
    </ul>
  </li>
</ul>

<h2 id="testing">Testing</h2>

<h3 id="leave-one-out">Leave-One-Out</h3>
<p>Leave-One-Out (L1O) testing involves taking a rating in your dataset, running a prediction on it as it it doesn’t exist, and then comparing the prediction with actual rating.</p>

<h3 id="measuring-accuracy-with-root-means-squared-error">Measuring Accuracy with Root Means Squared Error</h3>
<p>Root means squared error (RMSE) is the primary metric in which the accuracy of a prediction technique. It takes the root mean of all of the prediction accuracies and then squares it to ensure the result is a positive number.
<script type="math/tex">|\overline{E}|=\frac{\displaystyle\sum_{i=1}^{N}|p_i-r_i|^2}{N}</script></p>

<h3 id="measuring-coverage">Measuring Coverage</h3>
<p>Coverage is the amount of ratings possible when using a certain set of parameters within a prediction technique. For example, Mean item Rating uses all available ratings to create it’s prediction so it can always generate a prediction, but later we will see the use of minimum similarity neighborhoods, in which there are cases where a prediction isn’t possible. I calculated coverage with the equation below.</p>

<script type="math/tex; mode=display">Coverage(data)=\frac{\displaystyle\sum_{item\in data}canRate(item)}{|data|}</script>

<h3 id="measuring-efficiency">Measuring Efficiency</h3>
<p>Efficiency is a measure of how fast a prediction technique takes to calculate. There is commonly a trade off to be had between efficiency, accuracy, and coverage. In this case, I utilized the <a href="https://docs.python.org/2/library/time.html">Python Time Library</a> to quantify the efficiency of a technique.</p>

<h2 id="baseline-prediction-with-mean-item-rating">Baseline Prediction with Mean Item Rating</h2>
<p><script type="math/tex">prediction(u_i, item_k) = \displaystyle\sum_{u_j\in users} rating(u_j, item_k)</script>
Mean item rating simply takes the average rating of an item and uses that as a prediction. This method is incredibly simple to implement, but is also naive because it treats every rating with equal value and didn’t take any other data into consideration. The use of data outside the mean rating is why the other formulas are much more successful.</p>

<h2 id="predictions-using-distance-based-similarity">Predictions Using Distance-Based Similarity</h2>

<p>The first serious approach utilizes Cosine and Pearsons similarity between users to build neighborhoods. From this neighborhood I took the mean item rating of the target movie and use this as my prediction. There are two types of neighborhoods ones created by setting a minimum similarity and ones created by limiting the size of the neighborhood. The neighborhoods constructed with minimum similarity were tested at a minimum of zero similarity all the way to ninety percent similarity, testing in increments of fifteen percent and the neighborhoods constructed with a neighborhood size was tested at values ranging from fifty to two hundred and fifty, testing in increments of fifty users. The outcomes of these tests are seen in the graphs below.</p>

<table>
  <thead>
    <tr>
      <th style="text-align: center">Minimum Similarity</th>
      <th style="text-align: center">Neighborhood Size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center"><img src="Graphs/Cosine Minimum Similarity.png" alt="Cosine Minimum Similarity" /></td>
      <td style="text-align: center"><img src="Graphs/Cosin Neighborhood Size.png" alt="Cosin Neighborhood Size" /></td>
    </tr>
    <tr>
      <td style="text-align: center"><img src="Graphs/Pearsons Minimum Similarity.png" alt="Pearsons Minimum Similarity" /></td>
      <td style="text-align: center"><img src="Graphs/Pearsons Neighborhood Size.png" alt="Pearsons Neighborhood Size" /></td>
    </tr>
  </tbody>
</table>

<h2 id="predictions-using-resnicks-formula">Predictions Using Resnick’s Formula</h2>

<p>Our last and most accurate approach was using Resnick’s Prediction Formula. We used both cosine and Pearsons to calculate similarity metrics and used each of those methods along with neighborhood building with maximum size and minimum similarity. Resnick’s Prediction Formula proved to be very slow in all cases, but capable of producing some of the most accurate results.</p>

<table>
  <thead>
    <tr>
      <th style="text-align: center">Resnick Minimum Similarity</th>
      <th style="text-align: center">Resnick Neighborhood Size</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center"><img src="Graphs/Resnick Minimum Similarity with Cosin Nighborhoods.png" alt="Resnick Minimum Similarity with Cosin Nighborhoods" /></td>
      <td style="text-align: center"><img src="Graphs/Resnick Neighborhood Size with Cosin Nighborhoods.png" alt="Resnick Neighborhood Size with Cosin Nighborhoods" /></td>
    </tr>
    <tr>
      <td style="text-align: center"><img src="Graphs/Resnick Minimum Similarity with Pearsons Nighborhoods.png" alt="Resnick Minimum Similarity with Pearsons Nighborhoods" /></td>
      <td style="text-align: center"><img src="Graphs/Resnick Neighborhood Size with Pearsons Nighborhoods.png" alt="Resnick Neighborhood Size with Pearsons Nighborhoods" /></td>
    </tr>
  </tbody>
</table>

<h2 id="references">References</h2>

<p>[Harper and Konstan 2015] F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. From ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages. DOI=http://dx.doi.org/10.1145/2827872</p>

<p>[Resnick, Iacovou, Suchak, Bergstrom, Bergstrom, and Riedl 1994] Paul Resnick, Neophytos Iacovou, Mitesh Suchak, Peter Bergstrom, John Riedl. 1994. GroupLens: An Open Architecture for Collaborative Filtering of Netnews. From Proceedings of ACM 1994 Conference on Computer Supported Cooperative Work, Chapel Hill, NC: Pages 175-186</p>
