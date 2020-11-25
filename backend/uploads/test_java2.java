public class Fibonacci {
    public static void main(String[] args) {
        int n = 10, d1 = 0, d2 = 1;
        System.out.print("First " + n + " terms: ");
        for (int j = 1; j <= n; ++j)
        {
            System.out.print(d1 + " + ");
            int sum = d1 + d2;
            d1 = d2;
            d2 = sum;
        }
    }
}