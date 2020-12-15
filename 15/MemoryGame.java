import java.time.Instant;

public class MemoryGame {
    final static int[] input = {1,12,0,20,8,16};


    public static void main(String[] args) {
        Instant start = Instant.now();
        int[][] history = new int[30_000_000][];
        for (int i = 0; i < 30_000_000; i++) {
            history[i] = new int[] {-1, -1};
        }
        Instant midPoint = Instant.now();
        int lastVal = -1;
        int t = 0;
        for (int i : input) {
            history[i][0] = t;
            lastVal = i;
            t++;
        }

        while (t < 30_000_000) {
            int[] prior = history[lastVal];
            int cur = (prior[1] == -1) ? 0 : prior[0] - prior[1];
            int[] histOfCur = history[cur];
            histOfCur[1] = histOfCur[0];
            histOfCur[0] = t;
            lastVal = cur;
            t++;
        }

        Instant end = Instant.now();
        System.out.println(lastVal);
        System.out.println(end.toEpochMilli() - start.toEpochMilli());
        System.out.println(midPoint.toEpochMilli() - start.toEpochMilli());
    }
}
