import tkinter as tk
from get_sentiment import reviews_analysis
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

pad=3
window = tk.Tk()
window.title("Welcome")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("{}x{}+0+0".format(width, height))

def frontPage():
    frontPageFrame = tk.Frame(window)
    welcomeText = tk.Label(frontPageFrame, 
                        text="Put the link of the product page!",)
    welcomeText.config(anchor=tk.CENTER, font=(44))

    emptyLabel1 = tk.Label(frontPageFrame, text="", height=1)

    textInput = tk.Entry(frontPageFrame, width=30)

    emptyLabel2 = tk.Label(frontPageFrame, text="", height=1)

    btn = tk.Button(frontPageFrame, text="Submit", font=(20), command=lambda: frontPageClick(textInput) if len(textInput.get()) else frontPage)
    btn.config(font=('Helvetica', '11'))

    welcomeText.pack()
    emptyLabel1.pack()
    textInput.pack()
    emptyLabel2.pack()
    btn.pack()
    return frontPageFrame


def frontPageClick(textInput):
    url = textInput.get()
    global mainFrame
    mainFrame.destroy()
    product_name, ratings, avg_rating, negative_reviews, sentiments = reviews_analysis(url)

    each_counts = sentiments.value_counts()
    positive_counts = each_counts.loc["POS"]
    try:
            negative_counts = each_counts.loc["NEG"]
    except:
            negative_counts = 0

    # Now go to details frame:
    newFrame = tk.Frame(window)
    newFrame.grid(row=0, column=0)
    
    labelInfo = tk.Label(newFrame, text="Product Name:")
    labelInfo.config(font='Helvetica 18 bold')
    labelInfo.grid(row=0, column=0)

    emptySpace1 = tk.Label(newFrame, text="", width=5)
    emptySpace1.grid(row=0, column=1)

    name = tk.Label(newFrame, text=product_name)
    name.config(font='Helvetica 12', wraplength=600)
    name.grid(row=0, column=2)

    horizontalSpacer1 = tk.Label(newFrame, text="", height=1)
    horizontalSpacer1.grid(row=1)

    ratingInfo = tk.Label(newFrame, text="Average Rating: ")
    ratingInfo.config(font='Helvetica 18 bold')
    ratingInfo.grid(row=2, column=0)

    emptySpace1.grid(row=2, column=1)

    ratings_text = tk.Label(newFrame, text=str(avg_rating))
    ratings_text.config(font='Helvetica 12 bold')
    ratings_text.grid(row=2, column=2)

    horizontalSpacer2 = tk.Label(newFrame, text="", height=1)
    horizontalSpacer2.grid(row=3)

    totalRatingInfo = tk.Label(newFrame, text="Total Ratings: ")
    totalRatingInfo.config(font='Helvetica 18 bold')
    totalRatingInfo.grid(row=4, column=0)

    emptySpace1.grid(row=4, column=1)

    total_ratings_text = tk.Label(newFrame, text=len(ratings))
    total_ratings_text.config(font='Helvetica 12 bold')
    total_ratings_text.grid(row=4, column=2)

    horizontalSpacer3 = tk.Label(newFrame, text="", height=1)
    horizontalSpacer3.grid(row=5)

    print("LEN: ", len(negative_reviews))
    if len(negative_reviews):
        improvementInfo = tk.Label(newFrame, text="Room for improvement: ")
        improvementInfo.config(font='Helvetica 18 bold')
        improvementInfo.grid(row=6, column=0)

        neg_reviews = ""
        for review in negative_reviews["title"]:
            neg_reviews += review + "\n"

        negative_reviews_text = tk.Label(newFrame, text=neg_reviews)
        negative_reviews_text.config(font='Helvetica 12')
        negative_reviews_text.grid(row=6, column=2)
    else:
        noNegativeInfo = tk.Label(newFrame, text="There are no negative reviews!")
        noNegativeInfo.config(font='Helvetica 12')
        noNegativeInfo.grid(row=6, column=0, columnspan=3)

    # horizontalSpacer4 = tk.Label(newFrame, text="", height=2)
    # horizontalSpacer4.grid(row=7)

    graphInfo = tk.Label(newFrame, text="Ratings Graph")
    graphInfo.config(font='Helvetica 18 bold')
    graphInfo.grid(row=0, column=5, columnspan=3)

    horizontalSpacer5 = tk.Label(newFrame, text="", height=1)
    horizontalSpacer5.grid(row=1, column=5, columnspan=3)

    unique_ratings = {}
    for i in range(1, 6):
        unique_ratings[i] = 0
        for rating in ratings:
            if int(rating) == i:
                unique_ratings[i] += 1
                
    figure1 = plt.Figure(figsize=(5,4))    
    ax1 = figure1.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure1, newFrame)
    chart_type.get_tk_widget().grid(row=2, rowspan=4, column=5, columnspan=3)
    ax1.bar(unique_ratings.keys(), unique_ratings.values())
    ax1.set_xlabel("Star Rating (1 to 5)")
    ax1.set_ylabel("Number of Ratings")
    ax1.set_title('Ratings')

    horizontalSpacer6 = tk.Label(newFrame, text="", height=1)
    horizontalSpacer6.grid(row=6, column=5, columnspan=3)

    responseInfo = tk.Label(newFrame, text="Product Response:")
    responseInfo.config(font='Helvetica 18 bold')
    responseInfo.grid(row=7, column=0, columnspan=3)

    figure2 = plt.figure(figsize=(5,4))
    ax2 = figure2.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure2, newFrame)
    chart_type.get_tk_widget().grid(row=7, rowspan=4, column=5, columnspan=3)
    ax2.bar(["Positive", "Negative"], [positive_counts, negative_counts])
    ax2.set_xlabel("Positive vs Negative Ratings")
    ax2.set_ylabel("Number of ratings")
    # ax2.set_title("Product Response")


mainFrame = frontPage()
mainFrame.pack(expand=True)


window.mainloop()