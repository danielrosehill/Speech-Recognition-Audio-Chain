Your task in this repository:

I use speech recognition / STT a lot. 

I have a few microphones that I alternate between depending upon how much space I have on my desk. But I want to apply a common audio chain to all of them.

Here are the typical optimisations I like for STT:

- Automatic gain control 
- Dereverb 
- De-essing (slight)
- Background noise cancellation: this can be "lightweight". This is my home desktop. The most significant background noise is a screaming baby - but that's only periodic!

The system uses Pipewire. 

While I've used Easy Effects (the GUI) I find it a bit cumbersome to use. 

I would prefer an implementation that autostarted on boot and which I could stop with a CLI if needed. I don't need any processing on output.

I can use Audacity to test filters.