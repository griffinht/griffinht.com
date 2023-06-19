a secret is something only you have

password - only you have it until you share it or the service has it
password - could be easily guessable then others have it as well

password derivation functions whatever those are called - bcrypt

if you have to roll your own - if you are asking  yourself questinos about salt + pepper then its time to not roll your own!




an identity is something only you have that does not have to be secret
    something you have
        a file on a computer
            can be read by virus
                this is can be cloned
        key
            can be lost
            can be cloned
        security key
            can be lost
            can be cloned probably
        your physical attributes - these are not secret but they are something only you have!
            you
                somebody knows its you - like your bank teller or friends
                defeated by somebody impersonating you
            your face
                secure until somebody scans your face for you
            your eyes
                secure until somebody scans your eyes for you
            your fingerprint
                secure until somebody scans your fingerprint for you
    something you know
        password in your head
            can be forgotten
            can still be seen by others
            can get tiring to put in, tempts to write it down
        solve a puzzle
        pick your fav picture
        answer a security question

entropy of each of these?





a password is an identity
you are an identity
    your face, eyes, fingerprint
your key is an identity
a group idenity is ok - as long as the members of a group have something that non members do not





secret based identity
    an identiy proven by a secret - password, random key, etc 
        how can this be proven?
        storing the secret
        client offers secret -> server checks if secret matches what they have on file
        but what if the server loses its secrets? data breach?
            "no we pinky promise not to lose ur data haha"
            this would give your identity (proven by the secret) to other people, making your identity non unique and insecure because it can't prove you are one single person who should be allowed
        can we make this impossible by design? yes!
        enter the humble key derivationg? function
            input -> function ->  output
            given an input, we must be able to find a unique output
                some non unique may be ok
                abc -> 123
                def -> 123
                bad hashing function! hashing collision!
            given an output, we must not be able to find the input
                123 -> ?
                123 -> abc
                bad hashing function! example base64
                or,
                    aaa -> 234
                    aba -> 845
                    abb -> 455
                    abc -> 123
                    uh oh! we just reverse eningeered opur hasing function!
            how can we design a good hashing function?
                given an input, we must be able to find a unique output
                    no collisions
                given an output, we must not be able to find the input
                    no reverse engineer!
                depends on what we are hashing
                    base64
                        reverse engineer!
                    md5
                        reverse engineer!
                    sha1
                        reverse engineer!
                        give historic examples
                    sha256
                        good
                        except for passwords!
                    how much entropy?
                        a lot: sha256 is fine! sha1 is not?
                            10101110101010
                            uiohawiuhasdf
                            (give base64 example)
                            a 64 bit string? how much entropy - compare entropies, give examples of the same entropy
                        a little: most user passwords
                            please enter your password - must be easy to type and remember
                            techniques for making good passworsd
                                the quick brown fox jumps over the lazy dog - how much entropy? link to entropy hashing sites
                                easy to remember, tells a story
                            bad password
                                aB!3@cf
                                hard to remember, easy to guess by a computer
                            we are going to need to make these harder to reverse engineer, because they are easy to precompute!
                                rainbow tables example, common dict words, examples in hjistory
                            use a passwrod derivationg function
                                sha256 - no good!
                                md5 def no good! not even for high entropy
                                base64
                                scrypt
                                bcrypt
                                argon2id
                                salt protecting against rainbow table
                        dbouel hashing/triple hashing
