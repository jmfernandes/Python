########################################
#
# tag.py
#
# Description:
#
#
# Author: Josh Fernandes
#
# Created: Jan 09, 2018
#
# Updated:
#
#
########################################

def tag(name, *content, cls=None, **attrs):
    """Generate one or more html tags"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                            for attr,value in sorted(attrs.items()))
    else:
        attr_str=''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                            (name,attr_str,c,name) for c in content)
    else:
        return '<%s%s />' % (name,attr_str)

print(tag('br'))
print(tag('p','hello'))
print(tag('p','hello','world'))
print(tag('p','hello',id=33))
print(tag('p','hello','world',cls='sidebar'))
print(tag(content='testing',name='img'))
my_tag = {'name':'img', 'title':'sunset boulevard','src':'sunset.jpg','cls':'framed'}
print(tag(**my_tag)) #prefacting my_tag with ** passes all items as serpeate argurments

def f(a,*,b,c): #items names after the star must be named keywords and are required
    return a,b,c

#f(1) # does not work
#f(1,2,3) # does not work
print(f(1,b=2,c=3))
