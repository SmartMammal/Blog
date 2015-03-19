from blog import app

#Date formatting filter
@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format) #Use strftime method to format the date correctly