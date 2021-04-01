from flask import Flask, render_template, request
import musicbrainzngs


app = Flask(__name__)
# api req info
agentAuth = musicbrainzngs.set_useragent(
            "audacityVinylTag",
            "0.1",
            "shimotsg@protonmail.com",
        )

@app.route("/")
def list_artists():
    query = request.args.get('artist', 1)

    tmp_mbquery_item = musicbrainzngs.search_artists(query)
    artist_mbid = tmp_mbquery_item['artist-list'][0]['id']
    mb_queryresult = musicbrainzngs.browse_releases(artist=artist_mbid, release_type='album', limit=500)
    mb_queryresult_listing = {}
    for items in mb_queryresult['release-list']:
        mb_queryresult_listing[items.get('id')] = musicbrainzngs.browse_recordings(release=items.get('id'), limit=500)
    return render_template("index.html",
                           albums=mb_queryresult['release-list'],
                           album_tracks=mb_queryresult_listing)


# @app.route('/form')
# def form():
#     app.route('/<artist>')
#     return render_template("form.html")


if __name__ == '__main__':
    app.run()
