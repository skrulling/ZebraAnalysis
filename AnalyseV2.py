import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.ticker import ScalarFormatter
import numpy as np

#This import is just to use the Seaborn style on plots
import seaborn as sns

from mpl_toolkits.mplot3d import Axes3D
plt.switch_backend('TkAgg')
style.use('ggplot')

def df_delete_on_word(dataframe, key_wrd):
    cols = [c for c in dataframe.columns if key_wrd not in c.lower()]
    dataframe = dataframe[cols]

    return dataframe

def df_contains(dataframe, key_wrd):
    cols = [c for c in dataframe.columns if key_wrd in c.lower()]
    dataframe = dataframe[cols]

    return dataframe

def refine_df(dataframe, key_wrd, key_num):
    cols = [c for c in dataframe.columns if c.lower()[:key_num] == key_wrd]
    dataframe = dataframe[cols]

    return dataframe


def count_fish(dataframe, key_wrd, key_num):
    fish_count = 0

    for c in dataframe.columns:
        if c[:key_num] == key_wrd:
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
            # Change the value here to filter out more, or less noise
            # in movement

            dataframe.ix[dataframe[new_column_name_x] < 2, new_column_name_x] = 0
            dataframe.ix[dataframe[new_column_name_y] < 2, new_column_name_y] = 0

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
        print("3) Plot/graph menu.")
        print("4) Look at current table.")
        print("5) Save current DataFrame as .txt or .xlsx ")
        print("6) Distance calculation menu.")
        print("8) Clean tables and make distance calculations for each fish")
        print("9) To exit the program")
        print("\n")
        user_choice = input("What would you like to do?:")
        print("")

        if user_choice == '1':
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

                print("Do you have a group average .txt to load as well?")
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
                        print("Could not find that file, is it located in the same folder as the program?\n")


                else:
                    load_run = False


        elif user_choice == '2':
            print("Which columns would you like to delete?")
            print("Type number of columns separated by space example:(1 4 5 6)\n")

            counter = 0
            for group in pd.DataFrame(df):
                counter = counter + 1
                print(str(counter) + ") " + group)
            user_bar_list = [int(x) for x in input().split()]

            counter = 0
            for group in pd.DataFrame(df):
                counter = counter + 1
                for number in user_bar_list:
                    if counter == number:
                        df.drop([group], axis=1, inplace=True)
                        print("Deleted column " + str(counter))
                    else:
                        continue




    # --------------- PLOTTING MENU ---------------------



        elif user_choice == '3':
            plot_run = True

            while plot_run:
                print("\n")
                print("#####  Welcome to the plotting main menu  #####")
                print("\n")
                print("1) Bar plot: Make a bar plot from desired columns.")
                print("2) Automatically make bar plot of all distance columns.")
                print("3) Line plot, pixels as Y and frames as X.")
                print("4) Hex density plot")
                print("5) Box plot. - Not yet implemented")
                print("6) Histogram plot for speed.")
                print("7) 3D-plot showing position over time.")
                print("9) Exit plot menu.")
                print("\n")

                plot_choice = eval(input("What would you like to do?: "))
                print("")



                if plot_choice == 1:
                    print("Which groups would you like to plot?")
                    print("Type number of groups separated by space example:(1 4 5 6)\n")

                    counter = 0
                    for group in pd.DataFrame(df):
                        counter = counter + 1
                        print(str(counter)+ ") " + group)
                    user_bar_list = [int(x) for x in input().split()]
                    bar_df = pd.DataFrame
                    bar_dict = {}
                    print(user_bar_list)

                    counter = 0
                    for group in pd.DataFrame(df):
                        counter = counter + 1
                        for number in user_bar_list:
                            if counter == number:
                                label_bar = input("What would you like to call "
                                                  "the column " + group + ": \n")
                                sum_col = pd.DataFrame.sum(df[group])
                                bar_dict[label_bar] = sum_col
                            else:
                                continue


                    try:
                        title_plot = input("What would you like the title to be?: ")
                        x_label = input("Label x-axis: ")
                        y_label = input("Label y-axis: ")
                        list_dict = [bar_dict]
                        bar_df = pd.DataFrame(list_dict)
                        ax = bar_df.plot.bar(title=title_plot)
                        ax.set_xlabel(x_label)
                        ax.set_ylabel(y_label)
                        plt.show()

                    except:
                        print("Something went wrong with the plotting.\n")

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
                        print("")

                        try:
                            antall_bar = count_fish(df, "dist", 4)
                        except:
                            print("Error, could not find fish count.\n")
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
                                try:

                                    ax = bar_df.plot.bar(title="Total distance covered per fish",
                                                         colormap='Vega20b')
                                    ax.set_xlabel("Fish")
                                    ax.set_ylabel("Distance (pixels)")
                                    plt.show()

                                except:
                                    print("Error")

                            elif error_choice == 1:

                                try:
                                    #bar_df = refine_df(bar_df, )
                                    error = bar_df.std(axis=1)
                                    print("The standard deviation over total distance traveled for the fish is:")
                                    print(error)
                                    ax = bar_df.plot.bar(yerr=error, title="Total distance covered per fish",
                                                         colormap='Vega20b')
                                    ax.set_xlabel("Fisk")
                                    ax.set_ylabel("Distance (pixels)")
                                    plt.show()

                                except:
                                    print("Something went wrong with the plot.")

                        except:
                            print("Something went wrong!!!!")

                    if bar_choice == 2:

                        print("Do you want standard deviation included in plot?")
                        error_choice = eval(input("'1' for YES, '0' for NO: "))
                        print("")

                        if error_choice == 0:
                            try:
                                df_avg_bar = df_avg.sum()
                                ax = df_avg_bar.plot.bar(title="Average total distance over groups")

                                # Forsøk på å skille MPP fra de andre ved farge.

                                #df_avg_bar = df_delete_on_word(df_avg, 'mpp')
                                #df_avg_bar = df_avg_bar.sum()
                                #df_avg_mpp = df_contains(df_avg, 'mpp')
                                #df_avg_mpp = df_avg_mpp.sum()
                                #fig, ax = plt.subplots(2)
                                #df_avg_bar.plot.bar(title="Average total distance covered per group",
                                #                         color='blue', ax=ax)
                                #df_avg_mpp.plot.bar(color='red', ax=ax)
                                #df_avg_mpp.plot(ax=ax)
                                #df_avg_bar.plot(ax=ax)

                            except:
                                print("Something went wrong with the plotting.")

                        elif error_choice == 1:
                            try:
                                df_avg_bar = df_avg.sum()
                                error = df_avg_bar.std(axis=0)
                                print("The standard deviation over the groups is:")
                                print(error)
                                ax = df_avg_bar.plot.bar(yerr=error, title="Average total distance covered per group",
                                                         colormap='Vega20b')

                            except:
                                print("Something went wrong with the plot.")

                        #ax.set_ylabel("Distance (pixels)")
                        #ax.set_xlabel("Groups")
                        plt.show()




             #  ---------         This choice for making a line plot       ---------


                if plot_choice == 3:
                    print("1) Line plot of all fish in current group.")
                    print("2) Line plot of group averages in the 'df_avg' DataFrame.")
                    line_choice = eval(input("Which line plot would you like?: "))

                    if line_choice == 1:
                        #Taking the cumulative sum over columns and making a new DataFrame to use for line plot
                        df2 = df.cumsum()
                        df2 = refine_df(df2, 'dist', 4)

                        ax = df2.plot(title="Total distance in pixels over frames, per fish",
                                      colormap='Vega20b')

                    elif line_choice == 2:
                        # Taking the cumulative sum over columns and making a new DataFrame to use for line plot
                        df2 = df_avg.cumsum()

                        ax = df2.plot(title="Total distance in pixels over frames, per group of fish",
                                      colormap='Vega20b')

                    ax.set_xlabel("Time(frames)")
                    ax.set_ylabel("Distance(pixels)")
                    plt.show()

                # ------- Hex Density Plot ---------

                if plot_choice == 4:
                    try:
                        hex_fish = eval(input("Which fish would you like to plot?(enter number): "))
                        ax = df.plot.hexbin(x='X'+str(hex_fish), y='Y'+str(hex_fish), gridsize=15,
                                            title="Fish-"+str(hex_fish))
                    except:
                        print("Something went wrong with the plot. Perhaps chosen fish number is"
                              " invalid")

                    ax.set_xlabel("X-coordinates")
                    ax.set_ylabel("Y-coordinates")
                    plt.show()

                # --------- Box Plot ---------
                '''
                if plot_choice == 5:
                    box_choice = eval(input("To plot fish, type '1'. To plot groups type '0': "))

                    if box_choice == 1:
                        try:
                            df_box = refine_df(df, "dist", 4)
                            for column in df_box:
                                df_box_sum = pd.DataFrame(columns=['sum_dist_fish'])
                                df_box_sum['sum_dist_fish'].append(df_box[column].sum())
                                df_box = pd.concat([df_box, df_box_sum], axis=1)
                            print(df_box)
                            #ax = df_box.plot.box(column=['sum_dist_fish'], title="Distanse per fisk")
                        except:
                            print("Something went wrong plotting fish.")

                    if box_choice == 0:
                        try:
                            ax = df_avg.plot.box(title="Distanse per gruppe fisk")
                        except:
                            print("Something went wrong with the Box plot.")
                    plt.show()
                    '''

                # --------- Speed plot in histogram----------

                if plot_choice == 6:
                    try:
                        hist_choice = eval(input("1) To plot all fish in DataFrame \n"
                                           "0) To choose which fish to plot: "))

                    except:
                        print("Invalid choice.")

                    if hist_choice == 1:
                        try:
                            hist_title = input("Enter title of plot: ")
                            df_speed = refine_df(df, "dist", 4)

                            # Makes all 0 values NaN, so they are not included in the histogram
                            for column in df_speed:
                                df_speed.ix[df_speed[column] < 2, column] = np.NaN


                            ax = df_speed.plot.hist(title=hist_title ,bins=20, logy=True, colormap='Vega20b')
                            ax.set_xlabel("Speed in pixels/frame.")
                            ax.set_ylabel("Number of frames spent in speed range.")
                            plt.show()
                        except:
                            print("Something went wrong with the histogram plot.")

                    if hist_choice == 0:
                        num_fish = count_fish(df, "dist", 4)
                        print("There are " + str(num_fish) + " fish in your DataFrame.")
                        hist_fish = eval(input("Which fish do you want to plot? (1-"
                                               + str(num_fish) + "): "))
                        try:
                            #column = "dist_fish_"+str(hist_fish)
                            #df_speed[column] = df[column]
                            #df_speed.ix[df_speed[column] < 2, column] = np.NAN
                            name_col = "dist_fish_"+str(hist_fish)

                            ax = df[name_col].plot.hist(
                                bins=20, logy=True, colormap='Vega20b',
                                title="Fish-"+str(hist_fish))

                            ax.set_xlabel("Speed in pixels/frame")
                            ax.set_ylabel("Number of frames spent in speed range.")
                            ax.set_yticks([1, 5, 10, 50, 100, 200, 500, 1000, 5000, 10000])
                            ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
                            plt.show()
                        except:
                            print("Something went wrong trying to make the histogram")

                # ---------- 3D PLOT -----------

                if plot_choice == 7:
                    num_fish = count_fish(df, "dist", 4)
                    print("There are " + str(num_fish) + " fish in your DataFrame.")
                    threed_line = eval(input("Which fish do you want to plot? (1-"
                                            + str(num_fish) + "): "))

                    try:
                        threed_plot = plt.figure().gca(projection='3d')
                        threed_plot.plot(df["X"+str(threed_line)], df["Y"+str(threed_line)], df.index)
                        threed_plot.set_title("Position in 2D space over time for fish " + str(threed_line))
                        threed_plot.set_xlabel("X-Coordinate")
                        threed_plot.set_ylabel("Y-Coordinate")
                        threed_plot.set_zlabel("Time/Frame")
                        plt.show()

                    except:
                        print("Something went wrong with the plot!")



                if plot_choice == 9:
                    plot_run = False


        elif user_choice == '4':
            try:
                print(df)
            except:
                print("No DataFrame found!, returning to main menu.")

        # -------------- SAVE FUNCTION ---------------

        elif user_choice == '5':
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


        elif user_choice == '6':
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
                    print("NOTE: This step will create a new column\n")
                    print("It will also create a new DataFrame called 'df_avg' where it will")
                    print("make this group's average appear, this is so that you can load")
                    print("a different group and do the same calculation, and now have both")
                    print("averages in the same DataFrame to compare them more easily.\n")

                    col_avg_name = "group_avg_dist_" + input("Name your group average column: ")
                    print("")
                    print("New column was named: " + col_avg_name)
                    print("")


                    try:
                        df[col_avg_name] = refine_df(df, 'dist', 4).mean(axis=1)
                        #df_sum_fisk = pd.DataFrame

                        #for column in refine_df(df, 'dist', 4):
                         #   df_sum_fisk[column] = df[column].sum()

                        #cols = [c for c in df.columns if c.lower()[:4] == 'dist']
                        #df[col_avg_name] = df[cols].mean(axis=1)
                        print("")
                        print("Total mean distance for the group:")
                        print(df[col_avg_name].sum())
                        print("Pixels over " + str(len(df.index)) + " frames.")
                        print("")
                        df_avg[col_avg_name] = df[col_avg_name]
                        #df_avg[col_avg_name + '_STD'] = df_sum_fisk.std()
                        print("Column " + col_avg_name + " was added to the DataFrame 'df_avg'.")

                    except:
                        print("Something went wrong")

                if distance_menu_choice == 9:
                    distance_menu = False
                    print("Exiting distance menu..")

        elif user_choice == '8':

            try:
                #Looks for all columns starting with 'x', and assuming this is the x-coordinate column
                #for a fish, so it counts it. If other columns start with 'x', count will be wrong.

                num_fish_count = count_fish(df, "X", 1)
                print(num_fish_count)
            except:
                print("Error, could not find number of fish in dataframe.")

            try:
                df = clean_calc(df, num_fish_count)
                print("DataFrame has been cleaned and distance calculations have been made.")
            except:

                print("Something went wrong")


        elif user_choice == '9':
            run = False
            print("Exiting program..")

        else:
            print("!!  Invalid choice  !!")
            print("Please choose an option from the menu, and type its respective number.")
            print("")


program()











