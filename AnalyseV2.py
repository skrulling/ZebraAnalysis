import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
plt.switch_backend('TkAgg')
style.use('ggplot')

def refine_df(dataframe, key_wrd, key_num):
    cols = [c for c in dataframe.columns if c.lower()[:key_num] == key_wrd]
    dataframe = dataframe[cols]

    return dataframe

def count_fish(dataframe, key_wrd, key_num):
    fish_count = 0

    for c in dataframe.columns:
        if c.lower()[:key_num] == key_wrd:
            fish_count = fish_count + 1

        else:
            continue

    return fish_count


def clean_calc(dataframe, num_fish):

    cols = [c for c in dataframe.columns if c.lower()[:3] != 'pro']
    dataframe = dataframe[cols]
    cols = [c for c in dataframe.columns if c.lower()[:3] != 'unn']
    dataframe = dataframe[cols]

    for rad in range(1, num_fish + 1):
        fish_x = "X" + str(rad)
        fish_y = "Y" + str(rad)
        new_column_name_x = "x_dist_" + str(rad)
        new_column_name_y = "y_dist_" + str(rad)

        try:
            dataframe[new_column_name_x] = dataframe[fish_x].diff()
            dataframe[new_column_name_y] = dataframe[fish_y].diff()

            # Make Them Smooth

            dataframe.ix[dataframe[new_column_name_x] < 1, new_column_name_x] = 0
            dataframe.ix[dataframe[new_column_name_y] < 1, new_column_name_y] = 0

        except:
            print("Oh noes, that did not go as planned!")

    for fisk in range(1, num_fish + 1):
        dist_axis = "dist_fish_" + str(fisk)
        dist_ax_x = "x_dist_" + str(fisk)
        dist_ax_y = "y_dist_" + str(fisk)
        try:
            dataframe[dist_axis] = dataframe[dist_ax_x] ** 2 + dataframe[dist_ax_y] ** 2
            dataframe[dist_axis] = np.sqrt(dataframe[dist_axis])
        except:
            print("Ups, something went wrong...")

    return dataframe


def program():
    run = True

    #Making this DataFrame for later use, it is dedicated to group averages
    df_avg = pd.DataFrame()

    while run:
        print("----- Main Menu -----")
        print("\n")
        print("1) To load in an array from .txt")
        print("2) Delete redundant columns.")
        print("3) Make a plot.")
        print("4) Look at current table.")
        print("5) Save current DataFrame as .txt or .xlsx ")
        print("6) Make distance calculation in new column.")
        print("8) Clean tables and make distance calculations for each fish")
        print("9) To exit the program")
        print("\n")
        user_choice = eval(input("What would you like to do?:"))
        print("")

        if user_choice == 1:
            load_run = True
            while load_run:

                file_name = input("Which file would you like to analyze?")
                print("")
                try:
                    df = pd.read_csv(file_name, sep="\t", header=0, )
                    print("File loaded to main DataFrame named 'df'.")
                except:
                    print("Could not find that file, is it located in the same folder as the program?")
                    print("")
                    load_run = False

                print("Do you have a group average .txt to load aswell?")
                print("If not: press 'ENTER'")
                print("If you do, type name the filename (ending with .txt).")
                print("")
                load_choice = input("Filename (if you do not have one, press 'ENTER'): ")
                print("")

                if load_choice is not "":
                    try:
                        df_avg = pd.read_csv(load_choice, sep="\t", header=0, )
                        print("File loaded to group avg DataFrame named 'df_avg'.")
                        print("")
                        load_run = False
                    except:
                        print("Could not find that file, is it located in the same folder as the program?")

                else:
                    load_run = False


        if user_choice == 2:
            remove = eval(input("How many columns do you want to delete?:"))

            for i in range(0, remove):
                drop_name = input("Name the column you want to remove:")
                try:
                    df.drop([drop_name], axis=1, inplace=True)
                except:
                    print("name did not match any columns")



    # --------------- PLOTTING MENU ---------------------



        if user_choice == 3:
            plot_run = True

            while plot_run:
                print("\n")
                print("#####  Welcome to the plotting main menu  #####")
                print("\n")
                print("1) Bar plot: Make a bar plot from desired columns.")
                print("2) Automatically make bar plot of all distance columns.")
                print("3) Line plot, pixels as Y and frames as X.")
                print("9) Exit plot menu")
                print("\n")

                plot_choice = eval(input("What would you like to do?: "))
                print("")



                if plot_choice == 1:
                    antall_bar = eval(input("How many columns do you want to plot?: "))
                    bar_df = pd.DataFrame
                    bar_dict = {}

                    for bars in range(0, antall_bar):
                        try:

                            name_bar = input("Which column would you like to plot?: ")
                            #name_bar = "dist_fisk_" + str(bars)
                            label_bar = input("Label: ")
                            #label_bar = "Fisk_" + str(bars)
                            #bar_plot = pd.DataFrame.sum(df[name_bar])
                            #bar_plot.plot.bar(label=label_bar)
                            sum_col = pd.DataFrame.sum(df[name_bar])
                            bar_dict[label_bar] = sum_col
                        except:
                            print("something went wrong.")
                            pass
                    try:
                        list_dict = [bar_dict]
                        bar_df = pd.DataFrame(list_dict)
                        #bar_df = pd.DataFrame.from_dict(bar_dict, orient="index")
                        #bar_df.plot(type="bar")
                        bar_df.plot.bar()
                        plt.show()
                    except:
                        print("Something went wrong with the plotting.")

             #   --------   AUTO BAR PLOT ------------

                if plot_choice == 2:
                    print("1) Make a bar plot using each fish.")
                    print("2) Make a bar plot using groups found in 'df_avg'.")
                    print("")
                    bar_choice = eval(input("What do you want to plot?: "))
                    print("")

                    if bar_choice == 1:
                        print("Do you want standard deviation included in plot?")
                        error_choice = eval(input("'1' for YES, '0' for NO: "))

                        try:
                            antall_bar = count_fish(df, "dist", 4)
                        except:
                            print("Error, could not find fish count.")
                        try:

                            bar_df = pd.DataFrame
                            bar_dict = {}

                            for bars in range(1, antall_bar+1):
                                name_bar = "dist_fish_" + str(bars)
                                label_bar = "Fish-" + str(bars)
                                sum_col = pd.DataFrame.sum(df[name_bar])
                                bar_dict[label_bar] = sum_col

                            list_dict = [bar_dict]
                            bar_df = pd.DataFrame(list_dict)
                            if error_choice == 0:

                                ax = bar_df.plot.bar(title="Total distance covered per fish")
                                ax.set_xlabel("Fisk")
                                ax.set_ylabel("Distance (pixels)")
                                plt.show()

                            elif error_choice == 1:
                                #bar_df = refine_df(bar_df, )
                                error = bar_df.std(axis=1)
                                print(error)
                                ax = bar_df.plot.bar(yerr=error, title="Total distance covered per fish", colormap='Dark2')
                                ax.set_xlabel("Fisk")
                                ax.set_ylabel("Distance (pixels)")
                                plt.show()



                        except:
                            print("Something went wrong!!!!")

                    if bar_choice == 2:
                        try:
                            ax = df_avg.plot.bar(title="Average total distance covered per group")
                            ax.set_ylabel("Distance (pixels)")
                            ax.set_xlabel("Groups")
                            plt.show()

                        except:
                            print("Something went wrong with the plotting.")




             #  ---------         This choice for making a line plot       ---------


                if plot_choice == 3:
                    print("1) Line plot of all fish in current group.")
                    print("2) Line plot of group averages in the 'df_avg' DataFrame.")
                    line_choice = eval(input("Which line plot would you like?: "))

                    if line_choice == 1:
                        #Taking the cumulative sum over columns and making a new DataFrame to use for line plot
                        df2 = df.cumsum()
                        cols = [c for c in df2.columns if c.lower()[:4] == 'dist']
                        cols = cols + [c for c in df2.columns if c.lower()[:5] == 'group']
                        df2 = df2[cols]

                        ax = df2.plot(title="Total distance in pixels over frames, per fish")

                    if line_choice == 2:
                        # Taking the cumulative sum over columns and making a new DataFrame to use for line plot
                        df2 = df_avg.cumsum()

                        ax = df2.plot(title="Total distance in pixels over frames, per group of fish")

                ax.set_xlabel("Time(frames)")
                ax.set_ylabel("Distance(pixels)")
                plt.show()
                    
                if plot_choice == 9:
                    plot_run = False


        if user_choice == 4:
            try:
                print(df)
            except:
                print("No DataFrame found!, returning to main menu.")

        # -------------- SAVE FUNCTION ---------------

        if user_choice == 5:
            print("1) to save as .txt")
            print("2) to save as excel format.")
            format_choice = eval(input("Which format to save in (1 or 2)?: "))


            if format_choice == 1:
                try:
                    print("Which DataFrame would you like to save?")
                    print("1) Main DataFrame, contains x, y coordinates and any calculations done on each fish.")
                    print("2) Groupd average DataFrame, contains calculated group average distances.")
                    save_choice = eval(input("1 or 2: "))
                    new_name = input("New file name (must end with .txt): ")
                    if save_choice == 1:

                        df = df.round(2)
                        df.to_csv(new_name, sep="\t", index=False)

                    elif save_choice == 2:
                        df_avg = df_avg.round(2)
                        df_avg.to_csv(new_name, sep="\t", index=False)

                except:
                    print("Something went wrong :( ")

            if format_choice == 2:
                try:
                    new_name = input("New file name (must en with .xlsx): ")
                    writer = pd.ExcelWriter(new_name, engine="xlsxwriter")
                    df = df.round(2)
                    df.to_excel(writer, "Sheet-main")
                    df_avg.to_excel(writer, "Sheet-group-avg")
                    writer.save()
                except:
                    print("Something went wrong.")


        # ----------- DISTANCE CALCULATIONS MENU -------------------


        if user_choice == 6:
            distance_menu = True
            while distance_menu:
                print("\n")
                print("#### Welcome to the distance calculations menu ####")
                print("\n")
                print("1) Sum distance for all frames over a column.")
                print("2) Do group average distances. ")
                print("9) Exit menu")
                print("\n")

                distance_menu_choice = eval(input("What would you like to do?: "))


                if distance_menu_choice == 1:
                    sum_column = input("Which column do you want to take the sum of?: ")
                    try:
                        sum_num = pd.DataFrame.sum(df[sum_column])
                        print("The sum of all numbers in this column is: " + str(sum_num))
                    except:
                        print("Uh, something went terribly wrong.")

                # - Mean distance for group -

                if distance_menu_choice == 2:
                    print("NOTE: This step will create a new column")
                    print("It will also create a new DataFrame called 'df_avg' where it will")
                    print("make this group's average appear, this is so that you can load")
                    print("a different group and do the same calculation, and now have both")
                    print("averages in the same DataFrame to compare them more easily.")

                    col_avg_name = "group_avg_dist_" + input("Name your group average column: ")
                    print("")
                    print("New column was named: " + col_avg_name)


                    try:
                        cols = [c for c in df.columns if c.lower()[:4] == 'dist']
                        df[col_avg_name] = df[cols].mean(axis=1)
                        print("")
                        print("Total mean distance for the group:")
                        print(df[col_avg_name].sum())
                        print("Pixels over " + str(len(df.index)) + " frames.")
                        print("")
                        df_avg[col_avg_name] = df[col_avg_name]
                        print("Column " + col_avg_name + " was added to the DataFrame 'df_avg'.")

                    except:
                        print("Something went wrong")

                if distance_menu_choice == 9:
                    distance_menu = False
                    print("Exiting distance menu..")

        if user_choice == 8:
            #num_fish = eval(input("How many fish are in this group?: "))
            try:
                #Looks for all columns starting with 'x', and assuming this is the x-coordinate column
                #for a fish, so it counts it. If other columns start with 'x', count will be wrong.
                num_fish_count = count_fish(df, "x", 1)
                print(num_fish_count)
            except:
                print("Error, could not find number of fish in dataframe.")

            try:
                df = clean_calc(df, num_fish_count)
                print("DataFrame has been cleaned and distance calculations have been made.")
            except:

                print("Something went wrong")


        if user_choice == 9:
            run = False
            print("Exiting program..")


program()











