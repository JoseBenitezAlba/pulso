package es.pulso.music;
import android.net.Uri;
public class Song {
 public long id,albumId,duration; public String title,artist,album; public Uri uri;
 public Song(long i,long a,long d,String t,String r,String b,Uri u){id=i;albumId=a;duration=d;title=t;artist=r;album=b;uri=u;}
 public String subtitle(){return artist.equals("<unknown>") ? album : artist;}
 public static String time(long ms){long s=ms/1000; return (s/60)+":"+String.format(java.util.Locale.ROOT,"%02d",s%60);}
}
