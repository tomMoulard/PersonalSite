A Pen created at CodePen.io. You can find this one at http://codepen.io/pixelthing/pen/zGZKaQ.

 A widget to allow smooth transition between poster frame, youtube video and back.

* Fully responsive (16:9 and 4:3 variations)
* Not using the Youtube js API (only because it's another http call and we'd use barely any of it)
* Smooth transition between poster and video
* videoStop() script, useful for buttons or javascript events (eg closing modals), that removes the src of the youtube video, preventing it from playing after it's hidden. Can be targeted at a particular video, or all on the page.
* Delegated click event, allowing the video element to be ajaxed in after page initilisation, and still work.