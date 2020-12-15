import java.time.Instant;

public class MemoryGame {
    final static int[] input = {1,12,0,20,8,16};


    public static void main(String[] args) {
        Instant start = Instant.now();
        int[][] history = new int[30_000_000][];
        int lastVal = -1;
        int t = 0;
        for (int i : input) {
            if (history[i] == null) {
                history[i] = new int[] {t, -1};
            }
            history[i][0] = t;
            lastVal = i;
            t++;
        }

        while (t < 30_000_000) {
            int[] prior = history[lastVal];
            int cur = (prior[1] == -1) ? 0 : prior[0] - prior[1];
            int[] histOfCur = history[cur];
            if (histOfCur == null) {
                history[cur] = new int[] {t, -1};
            } else {
                histOfCur[1] = histOfCur[0];
                histOfCur[0] = t;
            }
            lastVal = cur;
            t++;
        }

        Instant end = Instant.now();
        System.out.println(lastVal);
        System.out.println(end.toEpochMilli() - start.toEpochMilli());
    }
}
