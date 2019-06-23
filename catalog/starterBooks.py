from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Book, User

engine = create_engine('sqlite:///booksCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# --Create a Dummy User--------------------------------------------------------
dummyUser = User(name="Hermione Granger", email="h.granger@gmail.com")
session.add(dummyUser)
session.commit()

# --Creating Starter books for the book catalog database-----------------------
book = Book(user_id=1, title="Uprooted", urlSafeTitle="uprooted",
            author="Naomi Novik",
            description=("A young village woman named Agnieszka, is born in" +
                         " a year where she is eligible to be taken by the" +
                         " Dragon - a powerful wizard who protects her" +
                         " village and the rest of the kingdom from the" +
                         " encroaching evil of the poisoned Wood."),
            genre="fantasy")
session.add(book)
session.commit()

book = Book(user_id=1, title="There's No Place Like Here",
            urlSafeTitle="theres-no-place-like-here",
            author="Cecelia Ahern",
            description=("One minute Sandy is jogging through the park, the" +
                         " next, she can't figure out where she is. The path" +
                         " is obscured. Nothing is familiar. A clearing up" +
                         " ahead reveals a camp site, and it's there that" +
                         " Sandy discovers the impossible: she has" +
                         " inadvertently stumbled upon the place-- and" +
                         " people--she's been looking for all her life, a" +
                         " land where all the missing people go."),
            genre="magical-realism")
session.add(book)
session.commit()

book = Book(user_id=1, title="The Scarlet Letter",
            urlSafeTitle="the-scarlet-letter",
            author="Nathaniel Hawthorne",
            description=("In June 1642, in the Puritan town of Boston, a" +
                         " crowd gathers to witness an official punishment." +
                         " A young woman, Hester Prynne, has been found" +
                         " guilty of adultery and must wear a scarlet A on" +
                         " her dress as a sign of shame."),
            genre="classic")
session.add(book)
session.commit()

book = Book(user_id=1, title="Pride and Prejudice",
            urlSafeTitle="pride-and-prejudice",
            author="Jane Austen",
            description=("A humorous story of love and life among English" +
                         " gentility during the Georgian era. Mr Bennet is" +
                         " an English gentleman living in Hartfordshire" +
                         " with his overbearing wife. The Bennets 5" +
                         " daughters; the beautiful Jane, the clever" +
                         " Elizabeth, the bookish Mary, the immature Kitty" +
                         " and the wild Lydia."),
            genre="classic")
session.add(book)
session.commit()

book = Book(user_id=1, title="Fahrenheit 451",
            urlSafeTitle="fahrenheit-451",
            author="Ray Bradbury",
            description=("At first, Guy Montag takes pleasure in his" +
                         " profession as a fireman, burning illegally" +
                         " owned books and the homes of their owners." +
                         " However, Montag soon begins to question the" +
                         " value of his profession and, in turn, his life."),
            genre="classic")
session.add(book)
session.commit()

book = Book(user_id=1, title="Meet the Frugalwoods",
            urlSafeTitle="meet-the-frugalwoods",
            author="Elizabeth Willard Thames",
            description=("The deeply personal story of how award-winning" +
                         " personal finance blogger Elizabeth Willard" +
                         " Thames abandoned a successful career in the city" +
                         " and embraced frugality to create a more" +
                         " meaningful, purpose-driven life, and retire to a" +
                         " homestead in the Vermont woods at age thirty-two" +
                         " with her husband and daughter."),
            genre="non-fiction")
session.add(book)
session.commit()

book = Book(user_id=1, title="Walt Disney: An American Original",
            urlSafeTitle="walt-disney-an-american-original",
            author="Bob Thomas",
            description=("Disney's trials and tribulations from being a" +
                         " driver in France for the Red Cross during World" +
                         " War One to planning a theme park. It also" +
                         " focused on Disney's skills and ideas he strove" +
                         " to create, and the obstacles he had to overcome." +
                         " The life that Disney carved for himself and all" +
                         " of America to admire has been completely" +
                         " uncovered in this book. His life showed that" +
                         " and ordinary boy, born poor at the turn of the" +
                         " century, could accomplish world fame and" +
                         " dominance."),
            genre="non-fiction")
session.add(book)
session.commit()

book = Book(user_id=1, title="Peter Pan",
            urlSafeTitle="peter-pan",
            author="J.M. Barrie",
            description=("The story of a mischievous little boy who can" +
                         " fly, and his adventures on the island of" +
                         " Neverland with Wendy Darling and her brothers," +
                         " the fairy Tinker Bell, the Lost Boys, the" +
                         " Indian princess Tiger Lily, and the pirate" +
                         " Captain Hook."),
            genre="classic")
session.add(book)
session.commit()

book = Book(user_id=1, title="My Name is Memory",
            urlSafeTitle="my-name-is-memory",
            author="Ann Brashares",
            description=("Daniel has spent centuries falling in love with" +
                         " the same girl. Life after life, crossing" +
                         " continents and dynasties, he and Sophia (despite" +
                         " her changing name and form) have been drawn" +
                         " together-and he remembers it all. Daniel has" +
                         " \"the memory\", the ability to recall past lives" +
                         " and recognize souls of those he's previously" +
                         " known. It is a gift and a curse. For all the" +
                         " times that he and Sophia have been drawn together" +
                         " throughout history, they have also been torn" +
                         " painfully, fatally, apart. A love always too" +
                         " short."),
            genre="young-adult")
session.add(book)
session.commit()

book = Book(user_id=1, title="How to Walk Away",
            urlSafeTitle="how-to-walk-away",
            author="Katherine Center",
            description=("Margaret Jacobsen has a bright future ahead of" +
                         " her: a fiance she adores, her dream job, and the" +
                         " promise of a picture-perfect life just around the" +
                         " corner. Then, suddenly, on what should have been" +
                         " one of the happiest days of her life, everything" +
                         " she worked for is taken away in one tumultuous" +
                         " moment."),
            genre="romance")
session.add(book)
session.commit()

book = Book(user_id=1, title="Little Moments of Love",
            urlSafeTitle="little-moments-of-love",
            author="Catana Chetwynd",
            description=("Little Moments of Love is a sweet collection of" +
                         " comics about the simple, precious, silly," +
                         " everyday moments that make up a relationship."),
            genre="humor")
session.add(book)
session.commit()

book = Book(user_id=1, title="Must Love Dogs",
            urlSafeTitle="must-love-dogs",
            author="Claire Cook",
            description=("Divorced preschool teacher Sarah Hurlihy's first" +
                         " mistake is letting her bossy big sister write her" +
                         " personal ad. Her second mistake is showing up to" +
                         " meet her first date in more than a decade. Now" +
                         " she's juggling her teaching job, her big," +
                         " rollicking, interfering south-of-Boston Irish" +
                         " family, and more men than she knows what to do" +
                         " with. And what's up with all these dogs that are" +
                         " suddenly galloping into her life?"),
            genre="romance")
session.add(book)
session.commit()

book = Book(user_id=1, title="The Truth About Forever",
            urlSafeTitle="the-truth-about-forever",
            author="Sarah Dessen",
            description=("Macy's summer stretches before her, carefully" +
                         " planned and outlined. She will spend her days" +
                         " sitting at the library information desk. She will" +
                         " spend her evenings studying for the SATs. Spare" +
                         " time will be used to help her obsessive mother" +
                         " prepare for the big opening of the townhouse" +
                         " section of her luxury development. But Macy's" +
                         " plans don't anticipate a surprising and chaotic" +
                         " job with Wish Catering, a motley crew of new" +
                         " friends, or ... Wes."),
            genre="young-adult")
session.add(book)
session.commit()

book = Book(user_id=1, title="The Belgariad",
            urlSafeTitle="the-belgariad",
            author="David Eddings",
            description=("A magnificent epic set against a history of seven" +
                         " thousand years of the struggles of Gods and Kings" +
                         " and men - of strange lands and events - of fate" +
                         " and a prophecy that must be fulfilled!"),
            genre="fantasy")
session.add(book)
session.commit()

book = Book(user_id=1, title="The Life-Changing Magic of Tidying Up",
            urlSafeTitle="the-life-changing-magic-of-tiding-up",
            author="Marie Kondo",
            description=("This book teaches you how to clean out your life" +
                         " by using the KonMari method created by Marie" +
                         " Kondo."),
            genre="non-fiction")
session.add(book)
session.commit()

book = Book(user_id=1, title="A Court of Thorns and Roses",
            urlSafeTitle="a-court-of-thorns-and-roses",
            author="Sarah J Maas",
            description=("When 19-year-old huntress Feyre kills a wolf in" +
                         " the woods, a beast-like creature arrives to" +
                         " demand retribution for it. Dragged to a" +
                         " treacherous magical land she only knows about" +
                         " from legends, Feyre discovers that her captor is" +
                         " not an animal, but Tamlin, one of the lethal," +
                         " immortal faeries who once ruled their world."),
            genre="fantasy")
session.add(book)
session.commit()

book = Book(user_id=1, title="Throne of Glass",
            urlSafeTitle="throne-of-glass",
            author="Sarah J Maas",
            description=("From his glass throne rules a King with a fist of" +
                         " iron and a soul as black as pitch. Assassin" +
                         " Celaena Sardothien won a brutal contest to become" +
                         " his Champion. Yet Celaena is far from loyal to" +
                         " the crown. She hides her secret vigilantly; she" +
                         " knows that the man she serves is bent on evil."),
            genre="fantasy")
session.add(book)
session.commit()

book = Book(user_id=1, title="The Host",
            urlSafeTitle="the-host",
            author="Stephenie Meyer",
            description=("Earth, in a post apocalyptic time, is being" +
                         " invaded by a parasitic alien race, known as" +
                         " \"Souls\", and follows one Soul's predicament" +
                         " when the consciousness of her human host refuses" +
                         " to co-operate with the taken over of her body."),
            genre="science-fiction")
session.add(book)
session.commit()

book = Book(user_id=1, title="Nancy Drew: The Secret of the Old Clock",
            urlSafeTitle="nancy-drew-the-secret-of-the-old-clock",
            author="Carolyn Keene",
            description=("Nancy, unaided, seeks to find a missing will. To" +
                         " the surprise of many, the Topham family will" +
                         " inherit wealthy Josiah Crowley's fortune, instead" +
                         " of deserving relatives and friends who were" +
                         " promised inheritances. Nancy determines that a" +
                         " clue to a second will might be found in an old" +
                         " clock Mr. Crowley had owned and she seeks to find" +
                         " the timepiece. Her search not only tests her keen" +
                         " mind, but also leads her into a thrilling" +
                         " adventure."),
            genre="mystery")
session.add(book)
session.commit()

print "Books Added!"
