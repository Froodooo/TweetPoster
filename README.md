# TweetPoster
TweetPoster is a small program written in Python that can automatically post (movie) quotes on Twitter. Setting up the program consists of two parts: (1) using the right command line arguments for the script and (2) set up a cronjob that executes the script at predefined moments in time.

## Python script
The program _script.py_ can be run using the following command line arguments:

```bash
python script.py -q <quotes file> -t <tokens file> -h <hashtag>
```

* The argument **-q** (or **--quotes**) must be followed by a file containing quotes. Each line of this file should contain one quote, consisting of the person to which the quote belongs and the actual quote itself. The format for this is as follows:

    ```
    <quote author>|<quote content>
    ```

* The argument **-t** or **--tokens** must be followed by a file containting four lines. The first two lines contain the consumer key and consumer secret key of a Twitter application. The last two lines contain the access token and access secret token of the Twitter account that will be used to post tweets. This account must allow the Twitter application access to its tokens, e.g. it should register (authenticate) itself with the application.
* The argument **h** must be followed by one hashtag that is placed at the end of the tweet.

The resulting tweet is of the following format:

```
"<quote content>" - <quote author> #<hashtag>
```

## Cronjob
In order to automatically post tweets on Twitter, you can use a Linux cronjob. In a Linux terminal, cronjobs can be set using the following command:

```bash
crontab -e
```

At the end of the file that now opens, you can enter a line like this one:

```bash
30 12 * * * ~/script.py
```

This line will execute the file _script.py_ every day at 12:30PM. [Consult this page for more information about _crontab_](http://ss64.com/bash/crontab.html), or just do a Google search yourself.
