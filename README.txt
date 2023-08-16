The following is my code repository for the research work I conducted under Juan Garbajosa during my stay at Universidad Politécnica de Madrid (UPM) in the summer of 2023. In regards to the context of the project, UPM’s Software Quality class has WhatsApp chats for team communication for the final class project. The goal of the project is to look at this communication between the team members and identify the personality types of each of the team members in order to understand what type of teams had the highest performance.

Here is a summary of what all the different files in this repository are for. The following Google Slides further explain the details of the project: https://docs.google.com/presentation/d/14nHqnchXnvvp6lmdiiMr-NoQX-55exVtb42jR_uSSko/edit?usp=sharing
If you have any questions related to anything found in this repository or the project in general, please don't hesitate to reach out to me at sharafr2@mit.edu.

The DistilBERT vocab and model files for the Fatherlander, Treehugger, Nerd, Spiritualist (Reddit) model is located in the following folder: distilbert_torch_reddit_model

The vocab and model files for the Ant, Bee, Leech (Spotify Podcasts) model is located in the following folder: distilbert_torch_spotify_antbeeleech_model

The data-sets folder contains the labeled data_sets used to train the DistilBERT models.

The interface is located in the file called "app.py". To launch the interface, simply run the app.py python file and then navigate to the local server that the terminal gives to host the interface. The associated HTML files for the interface are contained under the templates folder. A sample WhatsApp text file to try out the WhatsApp analysis feature is located under the data-sets folder.

The following files, bart_work_personality_classifier.py, trained_work_personality_classifier.py, tribe_personality_classifier.py, all contain the functions that rely on the trained models to allow you to classify a piece of text.

*There is one distinction between bart_work_personality_classifier and trained_work_personality_classifier. The distinction is that the Bart model uses three separate classifications of emotions from the Bart model to determine whether a piece of text is classified as an ant, bee, or leech. The trained model was the model that was trained on the labeled Spotify podcast dataset.

The following file, distillbert_nn_class.py, is the class used to load the trained models as can be seen in each of the classifier files. It was also used when initially training the models, and the code used to train the models can be found in the Google Colab Notebooks provided to Juan Garbajosa.

The file, post_retriever.py was the code I used in order to construct the labeled dataset for which the Fatherlander, Treehugger, Nerd, Spiritualist DistilBERT model was trained from. The file, podcast_processor.py, likewise, was the code I used in order to construct the labeled dataset for which the Ant, Bee, Leech DistilBERT model was trained from. It is important to note that the Spotify podcasts were obtained from the 2020 Spotify Podcast dataset which has the following citation:

Ann Clifton, Sravana Reddy, Yongze Yu, Aasish Pappu, Rezvaneh Rezapour, Hamed Bonab, Maria Eskevich, Gareth Jones, Jussi Karlgren, Ben Carterette, and Rosie Jones. 2020. “100,000 Podcasts: A Spoken English Document Corpus”. In Proceedings of the 28th International Conference on Computational Linguistics (COLING)

Last, the files: whatsapp_parser.py and whatsapp_profiler.py contain the functions used in the interface to process a WhatsApp text file_path and obtain each person's personality type classifications based on the messages they sent.

