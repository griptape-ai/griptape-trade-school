# Your SEO Friend

To really get the most out of your Griptape Agent for SEO purposes, you want to customize those image descriptions to perfection. After all, if we’ve heard it once, we’ve heard it a thousand times; if content is king, then well-optimized image metadata is the protected crown jewel in his majesty's collection. 

Let’s gear up to create metadata that not only enhances image accessibility but also gives you an SEO boost strong enough to make your competitors weep.

## Specific Requests for SEO-Friendly Information

First off, let's make sure our agent knows exactly what we’re looking for. Here’s how you could phrase a request that ticks all the SEO boxes:

```
Can you describe images/shoe.png for me in a way that would be SEO friendly? 
I would like an SEO description, keywords, an alt-description, and a caption 
that could go under the image on a web page.
```

For the shoe, the agent responds with:

```
Answer: Here are the SEO-friendly details for your image:

Description: The image features a vintage-style photo of a classic high-top 
sneaker placed on top of a weathered photo album, which lies on wooden planks. 
The warmth of the vintage tone conveys nostalgia, and the sneaker's laces 
appear slightly untied, suggesting a casual or well-worn theme.

Keywords: Vintage high-top sneaker, Retro photography, Shoe fashion, 
Casual footwear, Wooden background, Vintage photo album, Sneaker culture, 
Aesthetic nostalgia

Alt-Description: Vintage-inspired image of a classic high-top sneaker resting 
on an old photo album with wooden planks as a background.

Caption: Step Back in Time: A Classic Sneaker on Vintage Photo Album - 
A journey through retro fashion and cherished memories.
```

This command isn't just a request; it's an all-access pass to SEO town.

## Experiment with Different Requests

To optimize further, tweak your requests based on specific SEO strategies. Let's break down a few options:

### HTML Tag Generation

Ask your agent to whip up an example of an HTML image element optimized for SEO. It’s like asking it to dress up your image for a gala event—the right tags can make all the difference.

``` title="Prompt"
Can you give me an example of an HTML image element for the shoe that follows 
best SEO practices?
```

``` title="Agent"
Agent: Sure, here's an example of an HTML image element that 
follows best SEO practices:

<img src="images/shoe.png" 
    alt="Vintage-inspired image of a classic high-top sneaker resting on an 
    old photo album with wooden planks as a background." 
    title="Step Back in Time: A Classic Sneaker on Vintage Photo Album - 
    A journey through retro fashion and cherished memories."/>

In this example, the `src` attribute is the path to the image, the `alt` 
attribute provides an alternative description of the image for screen readers or 
in case the image fails to load, and the `title` attribute provides additional 
information about the image which can be displayed as a tooltip when the mouse 
moves over the image.
```

### Alt-text Limitation

Sometimes, less is more. Request alt-text with a character limit to keep it sweet and SEO-friendly, much like a good tweet.

``` title="Prompt"
I would like the alt-text, but limit it to under 125 characters.
```

``` title="Agent"
Agent: Sure, here's a shorter version of the alt-text that is under 125 characters:

Alt-Text: "Vintage high-top sneaker on an old photo album, wooden background."
```

### Keyword Variation

Experiment by asking for five keywords for the image, each from a different category

``` title="Prompt"
Give me 5 key words for this image, each in a different category.
```

``` title="Agent"
Agent: Sure, here are five keywords for the image, each representing a 
different category:

1. Fashion: "High-top sneaker"
2. Color: "Sepia-tone"
3. Style: "Vintage"
4. Material: "Wooden background"
5. Mood: "Nostalgia"
```

## Output Formats

Depending on the project's needs, you might require the information in various formats. Here are two examples:

### YAML Format

If YAML is your go-to format for configuration files or data storage (because who doesn’t like their data to be as stylish as it is structured?), here's how you can ask your Griptape Agent to deliver those SEO details:

``` title="Prompt"
Provide the following for the image in YAML format: SEO description, 
5 keywords, alt-text, caption, html image element.
```

``` title="Agent"
Agent: Sure, here is the requested information in YAML format:
```
```yaml
seo_description: "Vintage-style photo of a classic high-top sneaker placed on a weathered photo album, with a wooden background."
keywords: 
  - "High-top sneaker"
  - "Sepia-tone"
  - "Vintage"
  - "Wooden background"
  - "Nostalgia"
alt_text: "Vintage high-top sneaker on an old photo album, wooden background."
caption: "Step Back in Time: A Classic Sneaker on Vintage Photo Album - A journey through retro fashion and cherished memories."
html_image_element: "<img src='images/shoe.png' alt='Vintage high-top sneaker on an old photo album, wooden background.' title='Step Back in Time: A Classic Sneaker on Vintage Photo Album - A journey through retro fashion and cherished memories.'/>"
```

### JSON Format

Similarly, if you need to weave this data seamlessly into your web applications or databases, Jason is your guy. Just kidding, JSON isn’t a person. I learned that the embarrassing way. Here’s how you can request the same data in JSON format:

``` title="Prompt"
Provide the same in JSON
```

``` title="Agent"
Agent: Sure, here is the requested information in JSON format:
```
```json
{
  "seo_description": "Vintage-style photo of a classic high-top sneaker placed on a weathered photo album, with a wooden background.",
  "keywords": [
    "High-top sneaker",
    "Sepia-tone",
    "Vintage",
    "Wooden background",
    "Nostalgia"
  ],
  "alt_text": "Vintage high-top sneaker on an old photo album, wooden background.",
  "caption": "Step Back in Time: A Classic Sneaker on Vintage Photo Album - A journey through retro fashion and cherished memories.",
  "html_image_element": "<img src='images/shoe.png' alt='Vintage high-top sneaker on an old photo album, wooden background.' title='Step Back in Time: A Classic Sneaker on Vintage Photo Album - A journey through retro fashion and cherished memories.'/>"
}
```

---
## Next Steps

This structured approach to querying ensures that every piece of content generated by the agent is optimized for SEO, making the images more discoverable and enhancing the overall accessibility and user engagement of your website or application.

In the [next section](05_save_to_disk.md), make sure we can save this output to disk for us to use later.