

class FileTemplate(object):
    """Governs the reading and filling of file templates.
    Arguments:
       - filename: name of file that will eventually be written to

    Methods:
       - load_template: load given template for filling
       - fill_template: fill template using dictionary of fillers
       - set_value: replace a single tag with a filler
       - write: save file with previously defined replacements
    """

    def __init__(self, filename):
        "Save filename to write to and initialize content."
        self.filename = filename
        self.content = ''
        return

    def load_template(self, template_path):
        "Load template from given path to memory to be filled"
        with open(template_path, 'r') as f:
            self.content = f.read()
        return

    def set_value(self, tag, value):
        """Replace tag in template with value. 
        e.g. set_value('@USERNAME','thackray')
        """
        self.content = self.content.replace(tag, value)
        return

    def fill_template(self, fill_dict):
        """Take a dictionary of tag:value pairs and use them to fill template"""
        for tag in fill_dict:
            self.set_value(tag, fill_dict[tag])
        return

    def write(self, newfilename=None):
        """Save filled template to location newfilename. If newfilename is not
        given, save to location given in object initilization.
        """
        if newfilename:
            self.filename = newfilename
        with open(self.filename, 'w') as f:
            f.write(self.content)
