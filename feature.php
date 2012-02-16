<?php
$featuredata = json_decode(file_get_contents("caniuse-data.json"), true);
$browsers = array(
		  "opera" => array("id"=>"op_mob",
				   "x"=>130,
				   "y"=>8.8,
				   "width"=>60,
				   "height"=>60,
				   "url"=>"opera.png"),
		  "safari" => array("id"=>"ios_saf",
				    "x"=>0,
				    "y"=>8,
				    "width"=>60,
				    "height"=>60,
				    "url"=>"safari.jpg"),
		  "firefox" => array("id"=>"firefox",
				     "x" => 130,
				     "y" => 70,
				     "width" => 60,
				     "height" => 60,
				     "url"=>"firefox.png"),
		  "android" => array("id" => "android",
				     "x" =>65,
				     "y" =>0,
				     "width"=>60,
				     "height"=>69.9,
				     "url"=>"android.png"),
		  "bb" => array("id" => "blackberry",
				"x" => 0,
				"y" => 75,
				"width" => 60,
				"height" => 49.5,
				"url" => "blackberry.jpg"),
		  "ie" => array("id" => "ie",
				"x" => 63,
				"y" => 70,
				"width" => 60,
				"height" => 60,
				"url" => "ie.png")
		  );
		  
if ($featuredata[$_GET["name"]]) {
  header("Content-Type: image/svg+xml");
?><svg
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   width="260.30087"
   height="160.75708"
   version="1.1">
     <style typ="text/css">.unknown, .not { opacity: 0.3 } .partial { opacity: 0.5}</style>
<?php
     foreach($browsers as $id=>$data) {
     if ($featuredata[$_GET["name"]]["stats"][$data["id"]]) {
       $minVersion = 0;
       $minPartialVersion = 0;
       foreach($featuredata[$_GET["name"]]["stats"][$data["id"]] as $version=>$support) {
	 if ($support == "y") {
	   $minVersion = ($minVersion ? min($minVersion, $version) : $version);
	 } else if ($support == "a") {
	   $minPartialVersion = ($minPartialVersion ? min($minPartialVersion, $version) : $version);
	 }
       }
       if ($minVersion == 0) {
	 if ($minPartialVersion == 0) {
	   $supp = array("text" => array(attr => array("style" => "fill:red;font-size:40px;text-anchor:middle;"), "content" => "X", "offset" => array("y" => 10)));
	   $class ="not";
	 } else {
	   $supp = array("text" => array(attr => array("style" => "fill:#a70;font-size:20px;text-anchor:middle;"), "content" => $minPartialVersion . "+", "offset" => array("x" => 20, "y" => 30)));
	   $class ="partial";
	 }
       } else {
	 $supp = array("text" => array(attr => array("style" => "font-size:20px;text-anchor:middle;"), "content" => $minVersion . "+", "offset" => array("x" => "20", "y" => 30)));
	 $class ="";
       }
     } else {
       $supp = array("text" => array(attr => array("style" => "fill:blue;font-size:40px;text-anchor:middle;"), "content" => "?", "offset" => array("y" => 10)));
       $class="unknown";
     }
     echo "<image class='".$class."' xlink:href='".$data["url"]."' x='".$data["x"]."' y='".$data["y"]."' width='".$data["width"]."' height='".$data["height"]."' />\n";
     foreach ($supp as $el=>$values) {
       echo "<".$el;
       foreach($values["attr"]  as $attr=>$value) {
	 echo " $attr='".$value."'";
       }
       echo " x='".($data["x"] + $values["offset"]["x"] + $data["width"]/2)."'";
       echo " y='".($data["y"] + $values["offset"]["y"] + $data["height"]/2)."'";
       if ($values["content"]) {
	 echo ">".$values["content"]."</".$el.">\n";
       } else {
	 echo "/>\n";
       }
     }
  }
  echo "</svg>";
} else {
  echo "Pick a feature";
}
?>