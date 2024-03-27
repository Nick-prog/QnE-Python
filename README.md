[![LinkedIn][linkedin-shield]][linkedin-url]

# QnE-Python
 Python application equivalent to the Java Quick 'n' Easy counterpart.

 <div style="text-align:center">
  <img src="speede_server_image.jpg" alt="SPEEDE Server" />
  <img src="cross_symbol.jpg" alt="Cross Symbol" />
  <img src="python_symbol.jpg" alt="Python Symbol" />
 </div>

## What is Quick 'n' Easy?

Quick 'n' Easy (QNE) software is a free Java-based program developed by SPEEDE. It serves as a modern alternative to the traditional DOS platform, enabling users to print and acknowledge both college applications and high school transcripts. The software aims to streamline the process of handling transcripts and applications, making it more efficient and user-friendly.

Key features of Quick 'n' Easy software include:

1. **Java-Based Platform**: QNE is built on Java, making it platform-independent and accessible across various operating systems that support Java.

2. **Transcript Printing**: Users can easily print transcripts using the QNE software. This feature allows educational institutions to produce official transcripts quickly and efficiently.

3. **Transcript Acknowledgment**: QNE facilitates the acknowledgment of received transcripts. This feature is essential for institutions to confirm receipt of transcripts from other educational entities or students.

4. **Integration with SPEEDE Server**: The software seamlessly integrates with the SPEEDE server, a network service designed for the electronic exchange of student transcripts among educational institutions. This integration ensures compatibility and smooth transmission of transcript data.

5. **Testing with TST Files**: Upon downloading the QNE software, users are encouraged to test it with the SPEEDE server using TST files. This testing process allows users to familiarize themselves with the software's functionality and ensure its proper operation before handling actual transcript data.

## What is QnE-Python?

QnE-Python is a new project focusing on automating the transcript printing process, which is the second key feature of Quick 'n' Easy software. By leveraging Python scripting, QnE-Python aims to enhance the printing functionality of Quick 'n' Easy.

Key enhancements and features of QnE-Python:

1. **Automated Printing**: QnE-Python automates the printing process of transcripts generated by Quick 'n' Easy. This automation eliminates the need for manual intervention, improving efficiency and reducing the likelihood of errors.

2. **Enhanced Stability**: Unlike the Java-based Quick 'n' Easy software, QnE-Python offers improved stability by removing the need to reopen the application after printing 15 to 20 files. This enhancement ensures a smoother printing experience, particularly for large batches of transcripts.

3. **Future Compatibility**: QnE-Python has the potential to remain relevant for all future updates to the .spe file formats generated by Ellucian Banner, the commonly used student information system in educational institutions. Its adaptable architecture allows for easy integration with new file formats and specifications, ensuring long-term usability.

By focusing on automation and stability, QnE-Python provides a robust solution for transcript printing, enhancing the functionality of the Quick 'n' Easy software.

## Requirements

The QnE-Python script was written in a Python 3.9 environment. However, it can be run with any version of Python above 3.7 due to the main requirements of the reportlab library.

## How it Works

QnE-Python operates in several steps to automate the transcript printing process:

1. **Reading a .spe file and Creating a .csv file**: The application reads the target .spe file, extracts student information, and creates a .csv file for each student found within it.

2. **Sorting Applications**: It reads through the created .csv files to sort all foreign and domestic applications into lists for easier .pdf generation.

3. **Generating General Explanation**: The script identifies and interprets the markdown text within each list, providing a general explanation for each code encountered. For example, as of the making of this script, "BGN!" represents "Start of Application," "N3" represents "Address One," and "MSG" represents "Question Statement".

4. **Arranging Text on Pages**: The script arranges the general explanations (plain text) onto the right pages and locations based on a static set of logic.

5. **Rewriting Plain Text**: Finally, it rewrites the plain text into the given information in a format that is easier to read and understand for the user.

This systematic approach ensures efficient and accurate transcript and application printing, enhancing the overall usability of the Quick 'n' Easy software.

## How to Use the Application

Upon starting the application, the user will be prompted to select a .spe file of their choosing. Any other file selected will result in an error message.

The output will then be generated based on the location of the application itself in a folder path such as "C:/Users/Nick/Documents/QnE-Python/core/output/{name of .spe file}/{either domestic or foreign}/{found student's name}_{loop index}".

# Transforming the Cloned Repo into a software (.exe) application

To transform the cloned repo into a software .exe application, you can follow the step-by-step instructions provided in the [Publish Python Apps] under the Acknowledgements section for the cxfreeze-quickstart method. This method typically involves using tools like cx_Freeze to package Python applications into executable files.

Here's a brief overview of the process:

1. **Navigate to the Directory**: Open a terminal or command prompt and navigate to the directory containing your Python script.

2. **Create Setup.py File**: Create a `setup.py` file in the same directory as your Python script. This file will contain configuration information for building the executable.

3. **Specify Application Details**: Edit the `setup.py` file and specify details about your application, such as its name, version, description, author, and entry point (i.e., the main Python script).

4. **Build the Executable**: Use the cx_Freeze tool to build the executable. Run the appropriate command in your terminal or command prompt to generate the .exe file.

5. **Test the Executable**: Once the build process is complete, test the generated .exe file to ensure that it functions as expected.

The detailed instructions provided in the [Publish Python Apps] guide will walk you through each step, enabling you to successfully create a standalone executable from your Python script.

# Contact
Nickolas Rodriguez | Twitter: @\_Nick_Rod_ | Email: Nickolasrodriguez98@gmail.com | GitHub: Nick-prog

# Acknowledgements
* [Publish Python Apps](https://gist.github.com/ForgottenUmbrella/ce6ecd8983e76f6d8ef47e07240eb4ac)
* [SPEEDE application](https://www.speedeserver.org/using-speede/)

<!--MARKDOWN LINKS & IMAGES -->
 [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
 [linkedin-url]: https://linkedin.com/in/nickolas-rodriguez-392498197/
 
