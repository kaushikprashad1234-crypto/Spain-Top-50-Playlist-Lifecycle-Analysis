"# Spain-Top-50-Music-Lifecycle-Intelligence-Analysis" 
\documentclass[conference]{IEEEtran}
\usepackage{graphicx}
\usepackage{amsmath}

\title{Content Maturity, Lifecycle Dynamics, and Playlist Rotation: An Exploratory Analysis of Spain’s Top 50 Playlist}

\author{\IEEEauthorblockN{Kaushik Prasad}
\IEEEauthorblockA{Independent Researcher\\
Email: your-email@example.com}
}

\begin{document}

\maketitle

\begin{abstract}
This study analyzes lifecycle dynamics of songs in Spain’s Top 50 playlist using exploratory data analysis. Results indicate a high-churn ecosystem characterized by short lifecycles, rapid time-to-peak, and strong preference for new content. Content attributes such as explicit labeling and release format influence retention patterns. The findings provide actionable insights for optimizing release strategies and playlist performance.
\end{abstract}

\begin{IEEEkeywords}
Playlist Analytics, Lifecycle Analysis, Music Streaming, Churn, EDA
\end{IEEEkeywords}

% ===============================
\section{Introduction}
Streaming platforms have transformed music consumption, with playlists acting as primary discovery mechanisms. Spain represents a high-churn market where content lifecycle dynamics differ significantly from global averages.

% ===============================
\section{Methodology}

\subsection{Dataset}
Daily Top 50 playlist data including song metadata, ranking position, and content attributes.

\subsection{Lifecycle Metrics}
\begin{itemize}
\item Entry Date
\item Exit Date
\item Days on Playlist
\item Peak Position
\item Time to Peak
\end{itemize}

\subsection{Churn Analysis}
Churn is defined as the proportion of songs replaced daily.

% ===============================
\section{Results}

\subsection{Lifecycle Distribution}

\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{lifecycle_distribution.png}
\caption{Distribution of Days on Playlist}
\end{figure}

Most songs exhibit short lifecycles, with only a few achieving long-term retention.

% -------------------------------
\subsection{Time to Peak}

\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{time_to_peak.png}
\caption{Time to Peak Distribution}
\end{figure}

Songs reach peak performance early, indicating front-loaded engagement.

% -------------------------------
\subsection{Playlist Churn}

\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{churn_rate.png}
\caption{Daily Playlist Churn Rate}
\end{figure}

High churn confirms frequent playlist rotation.

% -------------------------------
\subsection{Average Position Stability}

\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{avg_position.png}
\caption{Average Position Over Time}
\end{figure}

Despite stable averages, internal playlist composition changes significantly.

% -------------------------------
\subsection{Content Maturity Analysis}

\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{explicit_vs_clean.png}
\caption{Explicit vs Non-Explicit Lifecycle}
\end{figure}

Non-explicit content shows slightly higher retention.

% -------------------------------
\subsection{Album vs Single Performance}

\begin{figure}[h]
\centering
\includegraphics[width=0.45\textwidth]{album_vs_single.png}
\caption{Album vs Single Lifecycle}
\end{figure}

Singles outperform album tracks in lifecycle duration.

% ===============================
\section{Discussion}

The Spanish music market demonstrates a compressed lifecycle model where songs rise and decline rapidly. Success is driven by early engagement and frequent content release.

% ===============================
\section{Strategic Implications}

\begin{itemize}
\item Focus marketing in first 7 days
\item Prioritize single releases
\item Increase release frequency
\item Optimize content attributes
\end{itemize}

% ===============================
\section{Conclusion}

Spain’s playlist ecosystem is high-churn and fast-moving, requiring data-driven strategies for success.

% ===============================
\begin{thebibliography}{00}

\bibitem{b1} Ò. Celma, \textit{Music Recommendation Systems}. Springer, 2010.

\bibitem{b2} C. Anderson, \textit{The Long Tail}. Hyperion, 2006.

\bibitem{b3} H. Datta et al., "Streaming and Music Consumption," Marketing Science, 2018.

\end{thebibliography}

\end{document}
