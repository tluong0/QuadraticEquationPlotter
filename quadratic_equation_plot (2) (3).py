from tkinter import *
import tkinter.messagebox as msg
import math

class CoefficientsDialog:


    def __init__(self, master, title = "Coefficients"):
        '''
        Create the window widgets
        '''
        self.a = 0
        self.b = 1
        self.c = 0
        self.top = Toplevel(master)
        if title:
            self.top.title(title)

        Label(self.top, text="X^2   +").grid(row=0,column = 1)
        Label(self.top, text="X     +").grid(row=1,column = 1)



        self.e1 = Entry(self.top)
        self.e2 = Entry(self.top)
        self.e3 = Entry(self.top)

        self.e1.grid(row=0)
        self.e2.grid(row=1)
        self.e3.grid(row=2)



        Button(self.top, text='Submit', command=self.submit).grid( rowspan = 2, row=3)




    def submit(self, event = None):
        '''
        Handle submit button action
        '''

		# dùng try catch hoặc str(self.a).isdigit() nếu check có phải digit hay ko
        self.a,self.b,self.c = self.e1.get(), self.e2.get(), self.e3.get()
        valid_input_a = True
        valid_input_b = True
        valid_input_c = True
        for i in self.a:
            if i in '0123456789-+':
                valid_input_a = True
            else:
                valid_input_a = False
                break
        for j in self.b:
            if j in '0123456789-+':
                valid_input_b = True
            else:
                valid_input_b = False
                break

        for k in self.c:
            if k in '0123456789-+':
                valid_input_c = True
            else:
                valid_input_c = False
                break

        if valid_input_a == True and valid_input_b == True and valid_input_c == True:
            self.a,self.b,self.c = self.e1.get(), self.e2.get(), self.e3.get()
            if(self.a == '0'):
                msg.showerror("Error", 'Coefficients of X^2 can not be 0')
                self.e1.delete(0,END)
                return
        else:
            msg.showerror("Error", 'Please enter valid input')
            self.e1.delete(0,END)
            self.e2.delete(0,END)
            self.e3.delete(0,END)
            return
		# check nếu là character??



		#(tùy)override X button 

        self.top.destroy()



class QuadEQPlot():

    def __init__(self,master):
        '''
        initialize any required data
        call init_widgets to create the UI
        '''

        self.a = 0
        self.b = 1
        self.c = 0


        self.x_value_sequence = range(-5,6)
        self.y_value_sequence = []
        for i in self.x_value_sequence:
            self.y_value_sequence.append(self.a*i + self.b*i + self.c)

        self.init_widgets(master)

        self.y_on_canvas = []





    def init_widgets(self,master):
        '''
        Create the window widgets and start the mainloop here
        You can call plot_axis to draw the inital x and y
        '''

        self.window = Toplevel(master)
        self.window.title("Function Plot")
        self.window.geometry("1000x600")

        menu_bar = Menu(self.window)

        file_menu = Menu(menu_bar, tearoff=False)
        file_menu.add_command(label = "New equation", command = self.new_equation)
        file_menu.add_command(label = "Save plot as .PS", command = self.save_canvas)
        file_menu.add_separator()
        file_menu.add_command(label = "Clear", command = self.clear_canvas)
        file_menu.add_command(label = "Exit", command = self.exit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Help", menu = help_menu)
        help_menu.add_command(label = "About", command = self.show_help_about)


        upper_frame = Frame(self.window)
        upper_frame.pack(expand = True, fill = X)


        self.v = StringVar()

        self.v.set("No equation")
        lb1 = Label(upper_frame, textvariable = self.v)
        lb1.pack(side = LEFT, anchor = W)

        self.plot_choice = IntVar()
        self.plot_choice.set(1)


        self.cnvs1 = Canvas(self.window,width = 1000, height = 2000)
        self.cnvs1.pack()



        options = ["Line", "Points"]
        rb1 = Radiobutton(upper_frame, text= options[0], variable = self.plot_choice, value = 0, command = self.plot_equation())
        rb1.pack(side = RIGHT, anchor = E)
        rb2 = Radiobutton(upper_frame, text = options[1], variable = self.plot_choice, value = 1,command = self.plot_equation())
        rb2.pack(side = RIGHT, anchor = E)




	
        #self.plot_axis()

        self.window.config(menu=menu_bar) 
		#self.plot_equation()

    def plot_axis(self):
        '''
        Draw x and y axis in the middle of the canvas
        '''

        self.cnvs1.create_line(500,50,500,550, width = 2, fill ="red")
        self.cnvs1.create_line( 250, 300, 750, 300, width=2, fill="blue")
        num = 0

        self.value_of_y_mark = []
        self.maximum_value_of_y = max((abs(min(self.y_value_sequence))),(abs(max(self.y_value_sequence))))
        print('max y' , self.maximum_value_of_y)

        self.distance = (self.maximum_value_of_y+5)//5
        print('distance', self.distance)
        for i in self.x_value_sequence:
            self.value_of_y_mark.append(i*(-self.distance))
        print(self.value_of_y_mark)
        #y axis
        for i in range(50,600,50):
            self.cnvs1.create_line(500,i,505,i,width = 2, fill ="red")

            self.cnvs1.create_text(490,i-5, text = self.value_of_y_mark[num], fill = "red")
            num+=1

        #x axis
        num =0
        for i in range(250,800,50):
            self.cnvs1.create_line(i,300,i,298,width = 2, fill ="blue")

            if self.x_value_sequence[num]!=0:
                self.cnvs1.create_text(i,300+7, text = self.x_value_sequence[num])
            num+=1

    def plot_equation(self,*args):
        '''
        plot the equation on canvas
        first clean the canvas, call plot_axis, calculate y values, and call either plot_points or plot_line
        '''


        if self.plot_choice.get() == 1:
                self.clear_canvas()
                self.plot_axis()
                self.plot_points()
                self.plot_line()

        if self.plot_choice.get() == 2:
                self.clear_canvas()
                self.plot_axis()
                self.plot_points()
        #if self.plot_choice==0:
        #self.plot_points()
        #else:
        #self.plot_line()

    def plot_points(self):
        '''
        for each x and y points, plot a 2x2 oval shape with a red border and yellow fill
        '''


        print('x cordinates', self.x_value_sequence)
        print('y cordinates', self.y_value_sequence)
        self.y_on_canvas = []
        for i in self.y_value_sequence:
            if i == 0:
                self.y_on_canvas.append(300)
            if i> 0:
                self.y_on_canvas.append(300-((500/2/(self.maximum_value_of_y+5))*i))
            if i <0:
                self.y_on_canvas.append(300+((500/2/(self.maximum_value_of_y+5))*-i))

        print('y on cavans', self.y_on_canvas)

        num = 0
        for i in range(250,800,50):
            self.cnvs1.create_oval(i,self.y_on_canvas[num],i,self.y_on_canvas[num], width=3)
            num +=1



    def plot_line(self,*scaled_points):
        '''
        using the (x, y) points, plot a smooth red line
        '''
        num = 0
        for i in range(250,800,50):
            if num < len(self.y_on_canvas)-1:
                self.cnvs1.create_line(i,self.y_on_canvas[num],i+50, self.y_on_canvas[num+1])
                num += 1


    def clear_canvas(self):
        '''
        triggered when the menu command 'Clear' is clicked
        delete everything from the canvas and set the coefficients to 0's
        '''
        self.cnvs1.delete("all")
    def new_equation(self):
        '''
        triggered when the menu command 'New Equation' is clicked
        call the child window to get the equation coefficients and then call plot_equation
        '''

        dial = CoefficientsDialog(self.window)
        self.window.wait_window(dial.top)

        self.a,self.b,self.c = int(dial.a), int(dial.b),int(dial.c)

        print('self.a = ', self.a,'self.b = ', self.b,'self.c = ', self.c)
        num = 0
        for i in self.x_value_sequence:
            self.y_value_sequence[num] = self.a*(i**2) + self.b*i + self.c
            num +=1
        print('x value sequences', self.x_value_sequence)
        print('y values sequences',self.y_value_sequence)

        equation = "" + str(self.a) + "X^2+ " +  str(self.b) + "X+ " + str(self.c)
        self.v.set(equation)

        self.plot_equation()







    def save_canvas(self):
        '''
        triggered when the menu command 'Save plot as .PS' is clicked
        save the graph as '{your_student_id_number}.ps'
        '''
        self.cnvs1.postscript(file="979613.ps", colormode='color')


    def exit(self):
        '''
        triggered when the menu command 'Exit' is clicked
        Ask if the user is sure about exiting the application and if the answer is yes then quit the main window
        '''

        if msg.askyesno("Exit", "Are you sure you want to exit?") == TRUE:
            self.window.quit()

    def show_help_about(self):
        '''
        triggered when the menu command 'About' is clicked
        Show an information dialog displaying your name on one line and id number on the second
        '''
        msg.showinfo("About QuadEQPlot", "Created by: Trang Luong \nID: 979613")

root=Tk()
root.withdraw()
q = QuadEQPlot(root)


root.mainloop()



