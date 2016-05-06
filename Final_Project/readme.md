
##Summary:
For my final project I wanted to focus on understanding the 

The imporant script generated reports: JavaLibReport.md and SakaiModuleReport.md in the reports folder

The meat of my project is a python script, generatemd.py, that parses dependency reports from maven and produces two markdown pages that allow the user to navigate the libraries that are implemented in Sakai. When executed in the base directory, given that Sakai has been properly deployed, the script will automatically query maven to get the dependency list and the dependency tree. From this it extractes a list of the Sakai modules and maps them to their imported libraries. Two markdown pages are then produced from this data, along with supplied csv data on the libraries(optional) and placed in the reports folder along with the other lists that were generated.

The important part, and reason for, generating the Markdown files is twofold. The markdown report allows link navigation among packages and modules. Additionally, when data on the libriaries(descriptions,links to documentation, categories) is filled into csvin.csv, the subcategories in JavaLibReport will contain useful info for the packages.

While this script is setup for Sakai, it should work for any maven build, although there are some filters that are specific to Sakai (ignoring imports from within the project)

##Initial Goals
 * Compare imports of Sakai 2.9 and 11
   *  This didn't go so well as I could not get Sakai 2.9 to compile fully to show all imports
 *   Develop some sort of interactive visulation with the dependecy data, like having tables where when you mousover a package it lights up the modules that use it
   *   This turned out to be way too ambitious as I have no JS experience!
   *   With most of my experience in Python, I instead decided to use it as a scripting language to parse the data, and to take advantage of the simplicty of markdown to generate web content on github.
   
##What ended up being created:
My intial goals of more complex web interfaces and data analysis did not match up with the time I could allocate to the project. Instead I settle with a proof of concept, a prototype of a script that can attach on to maven and provide a human readable report on the dependency strucure. This can be used for any maven project, and given proper development with fancy web interfaces, could provide visual interactive reports of the complex dependency structure found in large software projects

## Things to improve/expand:
*Right now you have to manually edit csvout and save as csvin before you can get the full script to run (you need at least five columns of data). It should be fairly straightforward to fix.
* The csv wiki needs to be filled in! A little bit of grunt work with ~100 entries.
* The string parsing is kludgy and likely not to be reliable across builds.
* More interative web design would be nice!
* Consider automatically generating the report upon deploying Sakai?
* One of the reasons for looking at imports is to understand why multiple versions of the sam JAR are being brought in. While the offending modules can be found in the markdown report, the scipt could be expanded to detect the repetitions and generate a seperate markdown file that details the issue.

## Things that were difficult
I was suprised how finicky proccesing my input files were. Even the tinies of spacing differences between different reports broke my code, and there are lots of kludges to fix this. While I tried to find any sort of method to parse the strings, there is probably a proper way to analyze the data and properly sanatize it. 


## Lessons:
For me this was a lesson in the neccesity of being familiar with a broader variety of languages and programming tools. My experience at Duke has only exposed me to Python, C++, C and Assembly working with basic command line programs. I had no prior experience with web or database work. It was frustrating knowing exactly what needed to be done, parsing maven reports into a data format and then generating a visual represetation of the data, but having to programming language skills to implement it. This is the other way around for something like algorithms or my OS class, where the hard part is working out how the algorithm was. I kept thinking if only I could control web interfaces with python while looking at javaScript D3 examples. Ultimately, I was happy to
