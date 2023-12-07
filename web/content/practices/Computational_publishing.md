Short description

Computational publishing broadly refers to publishing a book using techniques or processes from software development. This can include software development practices like forking, versioning, or programming and can produce books which incorporate computational elements alongside human-readable text such as executable code blocks, interactive visualisations, or browsable data repositories. 

Long description

'Computational publishing' is an umbrella term for a number of experimental publishing techniques and practices linked to the processes of software development. Broadly defined, it refers to publishing a book using techniques or processes from software development. 

Specialist software development practices like forking, versioning, or computer programming / scripting are generally only used in the production of computer software. Computational publishing involves using these practices in the production of a book. [Forking](https://compendium.copim.ac.uk/practices/59) and [versioning](https://compendium.copim.ac.uk/practices/66) are both given separate entries within this Compendium and involve taking software development practices—forking a code repository or using a version control system—and applying them to the authoring of a book publication. 

Since computational publishing is derived from the world of software development, a computational book will often contain computational elements within the publication itself. The computational functionality in computational books is distinguished from more basic computational functionality of e.g. hyperlinks by the extent to which it requires the use of techniques from software development such as writing in a programming language or automatically retrieving data or media objects through an API (application programming interface: a type of interface to allow two computer programs to communicate with one another and exchange data).

Experimental aspects

Computational book publications will generally combine human-readable text with computational functionality and generally use computational functionality in one of two ways.  

First, the human-readable text may comment on, interpret, or document the computational functionality. In a catalogue that was itself published using [GitHub Pages](https://compendium.copim.ac.uk/tools/3), [Andrew Odewahn (2015)](http://odewahn.github.io/patterns-of-code-as-media/www/introduction.html) refers to publications where "code is a media object in and of its own right". These texts allow the user to run code within the publication itself and [Odewahn (2015)](http://odewahn.github.io/patterns-of-code-as-media/www/introduction.html) aims to build a common vocabulary for communicating about code by categorising these publications that include code. The use of code as a media object may require some knowledge of programming languages for writing code that can be executed or in order to provide commentary on how the code operates. 

A good example of this kind of publication is [Winnie Soon & Geoff Cox’s (2020)](http://www.openhumanitiespress.org/books/titles/aesthetic-programming/) book *Aesthetic Programming: A Handbook of Software Studies* published by Open Humanities Press. As well as the 'frozen' hardcopy and PDF version of the book, the book is available as a [GitLab repository](https://aesthetic-programming.gitlab.io/book/) and as [a static site](https://www.aesthetic-programming.net/) generated from the repository. This allows the reader to actively run the various examples of JavaScript programming in the book in their web browser. Echoing Odewahn, [Soon & Cox (2020, p. 17)](http://www.openhumanitiespress.org/books/titles/aesthetic-programming/) write that "text is in code […] and code is in text":

> "the book sets out to express how writing and coding are deeply entangled, and how neither should be privileged over the other: we learn from their relationality. Writing code and writing about code are forced together in ways that reflect broader cultural and technical shifts in data practices and open publishing initiatives, and, moreover, emphasize that writing a book is necessarily a work in progress. Like software, this is a book to be read, and acted upon, shared and rewritten." 

As well as an author developing their own code to publish computationally, some online publishing platforms like [PubPub](https://compendium.copim.ac.uk/tools/15) allow for some degree of computational publishing via integration with sites like [CodePen](https://codepen.io/) which can render sample code blocks that combine HTML, CSS, and JavaScript. 

The second way that computational publications may integrate computational functionality is through incorporating digital media objects as an enhancement to the human-readable text. In a separate blog post, [Odewahn (2017)](https://github.com/odewahn/computational-publishing) identifies a few of the computational elements that can be incorporated as accompaniments to text: 

- interaction models such as plotting, mapping, or data visualisation
- media objects like video or audio
- executable code blocks
- data repositories housed on sites like GitHub, BitBucket, or GitLab

Some examples of these kinds of publications include [Simon Ganahl’s (2022) *Campus Medius: Digital Mapping in Cultural and Media Studies*](https://campusmedius.net/) which focuses on digital cartography by including interactive maps with explorable timelines around historical events, [Alexandra Juhasz’s (2011) *Learning From YouTube*](http://vectors.usc.edu/projects/learningfromyoutube/) which incorporates YouTube as both the subject and form of the 'video-book', and [Nicholas Bauch’s (2016) *Enchanting the Desert: A Pattern Language for the Production of Space*](http://www.enchantingthedesert.com/home/) which incorporates digital maps and photos alongside text. [Bret Victor’s (2011)](http://worrydream.com/ExplorableExplanations/) interactive essay 'Explorable Explanations' also provides examples of interactive visualisations that allow the reader to dynamically change the data represented encouraging what Victor refers to as "active reading". 

While some computational publishing software tools may make it easy to fetch or embed these kinds of computational media objects, they may also require the use of software development techniques to write code that expresses the object or to write code to retrieve the object from another source via an API.

Considerations

A major consideration for computational publishing is the specialist skills required. Since definitionally computational publishing uses techniques or processes from software development, then some familiarity is required not only with those techniques or processes but with the knowledge to understand how such software development processes interact. Software development is a specialist skill set and there’s a high technical complexity overhead in either contracting a developer to work on a computational publishing project or in learning the skills required to use specialist software. 

Computational publishing also requires a willingness to experiment and iterate perhaps more so than other experimental practices with more stable routes to an end goal. Many computational publishing projects link together a variety of software tools rather than using one single piece of software e.g. using [Jupyter Notebook](https://compendium.copim.ac.uk/tools/5) to create executable code blocks in Python, then using [Quarto](https://compendium.copim.ac.uk/tools/51) to render publication files, and then sending those to [GitHub Pages](https://compendium.copim.ac.uk/tools/3) for online hosting. This kind of complex technical workflow may be more difficult than using one single piece of proprietary software to write, edit, and typeset a publication but does allow for experimental and new techniques to be tried. 

This willingness to experiment also extends to publishers of computational books who in all likelihood would need to establish new workflows or heavily modify their existing workflows to accommodate the unique requirements of computational publications. [Adema (2023)](https://doi.org/10.21428/785a6451.30c8c105) explored these questions as part of COPIM's experimental publishing work package with particular consideration of how publishers need to consider "balanc[ing] the potential of more dynamic and interactive elements that a computational publication can offer with a requirement for more fixed and stable outputs to serve dissemination and preservation purposes."

Another consideration specific to computational publishing is reproducibility and digital preservation. Software development tools require a specific computational environment in order to function and consideration should be given to reproducing these environments in the future. This can be as simple as ensuring that Python is installed in order for someone to run a program but can involve setting up complex environments with tricky configurations. A full discussion of digital preservation for software is beyond the scope of this compendium entry but working with virtualization and containers in order to specify environment configurations can be a useful practice for computational publishing developers. 

Issues around preservation are complicated in the case of computational books by the issue of who is responsible for preserving external or remote content. [Adema (2023)](https://doi.org/10.21428/785a6451.2af49d16) discusses how dynamically bringing in content hosted by a third party creates the potential for link rot and content disappearing. Adema notes that Open Book Publishers has taken on responsibility for preserving URLs as Handles but not all publishers will either want to or be able to take on that kind of preservation work for third-party content.

Further reading

Bowie, S. (2022). What is computational publishing? *Community-Led Open Publication Infrastructures for Monographs (COPIM)*. [https://doi.org/10.21428/785a6451.af466093](https://doi.org/10.21428/785a6451.af466093)

Odewahn, A. (2017). Computational Publishing with Jupyter. In *GitHub*. [https://github.com/odewahn/computational-publishing](https://github.com/odewahn/computational-publishing)

Victor, B. (2011). Explorable Explanations. [http://worrydream.com/ExplorableExplanations/](http://worrydream.com/ExplorableExplanations/)




References (included here for posterity, not for publication)
 
Bauch, N. (2016). Enchanting the Desert: A Pattern Language for the Production of Space. Stanford University Press. http://www.enchantingthedesert.com/home/

Bowie, S. (2022). What is computational publishing? Community-Led Open Publication Infrastructures for Monographs (COPIM). https://doi.org/10.21428/785a6451.af466093

Ganahl, S. (2022). Campus Medius: Digital Mapping in Cultural and Media Studies. Transcript Publishing. https://campusmedius.net/ 

Juhasz, A. (2011). Learning From YouTube. The MIT Press. http://vectors.usc.edu/projects/learningfromyoutube/ 

Odewahn, A. (2017). Computational Publishing with Jupyter. In GitHub. https://github.com/odewahn/computational-publishing

Odewarn, A. (2015). Patterns of Code as Media. http://odewahn.github.io/patterns-of-code-as-media/www/introduction.html 

Soon, W., & Cox, G. (2020). Aesthetic Programming: A Handbook of Software Studies. Open Humanites Press. http://www.openhumanitiespress.org/books/titles/aesthetic-programming/

Victor, B. (2011). 'Explorable Explanations'. http://worrydream.com/ExplorableExplanations/ 