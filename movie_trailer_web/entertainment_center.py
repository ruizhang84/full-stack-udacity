import media
import fresh_tomatoes

#A list of movies
a_beautiful_mind = media.Movie("A Beautiful Mind",
                               "The life of John Nash, a Nobel Laureate in Economics.",
                               "https://upload.wikimedia.org/wikipedia/en/b/b8/A_Beautiful_Mind_Poster.jpg",
                               "https://youtu.be/JV2PSWSyi0s")
warcraft = media.Movie("Warcraft",
                       "Fantasy film based on the video game series of Warcraft",
                       "https://upload.wikimedia.org/wikipedia/en/5/56/Warcraft_Teaser_Poster.jpg",
                       "https://youtu.be/Zu8_wryd5r4")
transformers = media.Movie("Transformers: The Last Knight",
                           "Humans Are at War with the Transformer",
                           "https://upload.wikimedia.org/wikipedia/en/2/26/Transformers_The_Last_Knight_poster.jpg",
                           "https://youtu.be/6Vtf0MszgP8")
titanic = media.Movie("Titanic",
                      "American Epic Romance-disaster Film",
                      "https://upload.wikimedia.org/wikipedia/en/2/22/Titanic_poster.jpg",
                      "https://youtu.be/2e-eXJ6HgkQ")
godfather = media.Movie("The Godfather",
                        "The Transformation of Michael Corleone from Reluctant Family Outsider to Ruthless Mafia Boss",
                        "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
                        "https://youtu.be/dNE2PvbesQU")
steve_jobs = media.Movie("Steve Jobs",
                         "The Biographical Drama Film of Formal Apple CEO and co-founder Steve Jobs",
                         "https://upload.wikimedia.org/wikipedia/en/a/aa/SteveJobsposter.jpg",
                         "https://youtu.be/aEr6K1bwIVs")
movies = [a_beautiful_mind, warcraft, transformers, titanic, steve_jobs, godfather]

#open movie trailer website
if __name__ == '__main__':
    fresh_tomatoes.open_movies_page(movies)
