from __init__ import Main, gtk


if __name__ == "__main__":
    try:
        main = Main()
        gtk.main()
    except Exception as e:
        print(e)
