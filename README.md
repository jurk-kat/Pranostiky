# Kateřina na ledě, Vánoce na blátě - is it true?

The idea of conducting a study on whether Czech weather proverbs hold true or not was born on an autumn evening when I got into a debate with my Finnish girlfriend about the saying "Kateřina on ice, Christmas in mud". I described my teenage experiences to her: how on St. Catherine's Day, the first snow would fall, only for snowdrops to bloom by Christmas; and how one year - after 25th of November being muddy - the Christmas was white with to freezing temperatures. Thanks to the that the local pond was frozen and I became an excellent skater.

My partner rightly pointed out that drawing meaningful conclusions based on vague memories of a few years wasn’t exactly scientific — and I agree, that is correct. But hey, now I have the tools to look into it more analytically (thank you, Czechitas)! So, I downloaded a weather dataset spanning 50 years from OpenMeteo and created my first graphs. These already showed which years the proverb held true and which ones it didn’t. Nevertheless, I knew more in depth study would be needed.

For a while, I toyed with the idea of presenting the topic to the new students at Czechitas during the spring course of Digital Academy - Data. But at the same time, I couldn’t wait to see the actual results. Which years did the proverb hold true? In which places or parts of the country? Is it dependent on altitude? And what about other proverbs? Is there any year where all — or most of them - were fulfilled?

I decided not to wait and started working on the project on my own.

So far I have the coordinates & elevation data copied from https://www.chmi.cz/aktualni-situace/aktualni-stav-pocasi/ceska-republika/stanice/profesionalni-stanice/tabulky/zemepisne-souradnice?l=en for the trial. These are the locations of official Czech meteo stations. I might be looking into getiting data of the whole country in the future. At the moment I am writing these lines, I do not know yet.

For scraping the meteorological data, I decided to use the open meteo archive at https://archive-api.open-meteo.com/v1/archive . I already knew the page from my previous work on the DA project (https://github.com/jurk-kat/DA-projekt) so it was easier for me to work with that. I discovered a python code for api there as well. I decided to use it and rewrite a bit to fit better my needs. I need meteorological data from several locations and preferably in a more user friendly form than the automatic button based downloader on the site gives me. I am looking for the posibility also to get geographical data of the whole Cyech Rep and check the validity of the proverb in the whole area. That will be a lot of data so I might adjust the code more to download me only the data of the days I am interested in (25.11. and 24.12.).

I added also a gitignore file - some of the downloaded datasets were exceeding what I can upload in GitHub.

I will be updating this as I write more code and see where it takes me.
