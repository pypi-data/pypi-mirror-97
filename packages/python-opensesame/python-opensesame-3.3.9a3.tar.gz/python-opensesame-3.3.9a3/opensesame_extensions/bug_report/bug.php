<?php
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL);
// http://cogsci.nl/bug.php?platform=test&version=test2&python_version=test3&traceback=test4
$servername = "localhost";
$username = "cogscinl";
$password = "WUELDLpXm9kX5Wf";
$db = "cogscinl_osdoc";
// Create connection
$conn = new mysqli($servername, $username, $password, $db);
$platform = $conn->real_escape_string($_GET['platform']);
$version = $conn->real_escape_string($_GET['version']);
$python_version = $conn->real_escape_string($_GET['python_version']);
$traceback = $conn->real_escape_string($_GET['traceback']);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$sql = "INSERT INTO bug_reports (platform, version, python_version, traceback) VALUES ('$platform', '$version', '$python_version', '$traceback')";
$conn->query($sql);
$conn->close();
echo("OK");
?>
