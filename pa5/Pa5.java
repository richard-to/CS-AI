import java.io.*;

public class Pa5 {
    public static final String DELIM = " +";
    public static final String FILEPATH = "test-house-votes-1984.txt";
    public static final int NUM_FEATURES = 17;

    public static final int PHYSICIAN_FEE_FREEZE = 3;
    public static final int ADOPTION_OF_THE_BUDGET_RESOLUTION = 2;
    public static final int ANTI_SATELLITE_TEST_BAN = 6;
    public static final int PARTY = 16;

    public static final String NO = "n";
    public static final String YES = "y";
    public static final String DEMOCRAT = "democrat";
    public static final String REPUBLICAN = "republican";

    public static void main(String[] args) {
        try {
            File file = new File(FILEPATH);
            BufferedReader br = new BufferedReader(new FileReader(file));
            br.readLine();
            br.readLine();
            String line;

            float totalCorrect = 0;
            float total = 0;

            while ((line = br.readLine()) != null) {
                String[] tokens = line.split(DELIM);
                if (tokens.length == NUM_FEATURES) {
                    String prediction = predict(tokens);
                    String actual = tokens[PARTY];
                    Boolean correct= prediction.equals(actual);
                    if (correct) {
                        ++totalCorrect;
                    } else {
                        System.out.println(line);
                    }
                    ++total;
                    //System.out.println(correct + " " + prediction + " " + actual);
                }
            }
            System.out.println("-------------------");
            System.out.println(totalCorrect/total * 100 + " %");
        } catch (FileNotFoundException e) {
            System.err.println(e.getMessage());
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    public static String predict(String[] tokens) {
        String party = null;
        if (tokens[PHYSICIAN_FEE_FREEZE].equals(NO)) {
            party = DEMOCRAT;
        } else if (tokens[PHYSICIAN_FEE_FREEZE].equals(YES)) {
            if (tokens[ADOPTION_OF_THE_BUDGET_RESOLUTION].equals(YES)) {
                if (tokens[ANTI_SATELLITE_TEST_BAN].equals(NO)) {
                    party = DEMOCRAT;
                } else if (tokens[ANTI_SATELLITE_TEST_BAN].equals(YES)) {
                    party = REPUBLICAN;
                }
            } else if (tokens[ADOPTION_OF_THE_BUDGET_RESOLUTION].equals(NO)) {
                party = REPUBLICAN;
            }
        }
        return party;
    }
}
