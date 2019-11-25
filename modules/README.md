# Brain-Controlled-Flappy-Bird
This is a version of Flappy Bird that's controlled completely using your brainwaves! The program uses electroencephalography (or EEG) through the 2016 Muse headband to record the electromagnetic waves that our
brains emit.

The data from the Muse headband is received using the User Datagram Protocol (UDP), and then processed. When the program detects a blink (which is technically noise, or interference), the bird will flap.
Simply blink to make the bird flap!

### Usage
```sh
$ git clone https://github.com/karmdesai/Brain-Controlled-Flappy-Bird.git
$ cd Brain-Controlled-Flappy-Bird
$ python main.py <IP address> <Port>
```

The two parameters, **IP address** and **Port** should be replaced with the IP address of your computer and the port that you're streaming the data to, respectively. As an example:

```sh
$ python main.py 127.0.0.1 7000
```

Please note that a Muse headband and the Muse Direct application is required to collect and stream EEG data to the Python program.