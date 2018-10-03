''' class containing styles for each part of the gui '''
class styles:
    main_window = """
        QWidget{
            background-color: #222f3e;
            border-style: solid;
            border-width: 2px;
            border-radius: 10px;
            border-color: #0f0f0f;
            color: white;
            font: 12px;
            }
        """
    btn_remove = """
        QPushButton:hover {
                background-color: #ff6b6b;
                }
        QPushButton:pressed {
            background-color: #ff9f43;
            }
        QPushButton {
            background-color: #ee5253;
            font: 12px;
            border-radius: 3px;
            border-width: 2px;
            }
        """
    btn_finalize = """
        QPushButton:hover {
            background-color: #1dd1a1;
            }
        QPushButton:pressed {
            background-color: #ff9f43;
            }
        QPushButton {
            background-color: #10ac84 ;
            border-radius: 3px;
            border-width: 2px;
            }
        """
    view_file_widget = """
        QWidget{
            background-color: #8395a7;
            }
        """
    edit_widget = """
        QWidget{
            background-color: #576574;
            border-style: outset;
            border-width: 1px;
            border-radius: 5px;
            font: 12px;
            }
        """
    view_widget = """
        QWidget{
            background-color: #576574;
            border-style: outset;
            border-width: 1px;
            border-radius: 5px;
            }
        """
    title_labels = """
        QLabel{
            font:bold 14px;
            }
        """
    warning_label = """
        QLabel{
            font:bold 12px;
            color: #ff9f43;
            }
        """

    text_field = """
        QWidget:hover{
            background-color: #F5F5F5;
            color: black;
            }
        QWidget{
            background-color: white;
            color: black;
            }
        """