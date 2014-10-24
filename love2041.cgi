#!/usr/bin/perl
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Cookie;

require "page_browse.cgi";
require "page_profile.cgi";
require "helper_functions.cgi";

$login = param('login');
$password = param('password');
$directory = "./students";
$homePage = param('home_page'); 
$browsePage = param('browse_page'); 
$profilePage = param('profile_page');
$searchTerm = param('search_term');
$registerPage = param('register_page');
$person = param('view_person');
$pageNumber = param('page') || 0; 

if (defined $login && defined $password) {
my $u = CGI::Cookie->new (
    -name => 'username',
    -value => $login
);

my $p = CGI::Cookie->new 
(-name => 'password',
-value => $password);

print "Set-Cookie: $u\n";
print "Set-Cookie: $p\n";
}

print "Content-type: text/html\n\n";

print start_html (
    -title => "LOVE2041",
    -style => [
        { -src => "//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" },
        { -src => "http://fonts.googleapis.com/css?family=Oswald:400,700,300" },
        { -src => "http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" },
        { -src => "custom.css" },
    ]
);

if (authenticate()) { 
    if (defined $homePage) { 
        print '<center>';
        print '<h5> LOVE2041</h5>'; 
        loginPage();
        print goRegisterPage();
        print '</center>';
    } elsif (defined $browsePage || defined $searchTerm) { 
        browsePageHeader();
        browsePageContent();
    } elsif (defined $profilePage) { 
        browsePageHeader();
        profilePage();
    } else { 
        browsePageHeader();
        browsePageContent();
    } 
} elsif (defined $login && defined $password) { 
    print '<center>';
    print '<h5> LOVE2041</h5>';
    print 'Wrong login or password!<br>';
    loginPage();
    print goRegisterPage();
    print '</center>';
}  else {
    print '<center>';
    print '<h5> LOVE2041</h5>'; 
    loginPage();
    print goRegisterPage();
    print '</center>';
}

print '</html>';


sub authenticate {
    %cookies = CGI::Cookie->fetch;
    my $password = $cookies{'password'}->value;
    my $login = $cookies{'username'}->value;
    open $file, "username.txt" or die;
    $file = join ('', <$file>);
    @text = split("\n", $file);
    foreach $line (@text) { 
        if ($line eq "$login $password" ) { 
            return 1;
        }
    } 
    return 0; 
}


sub searchbar { 
    return 
        start_form,  
        textfield (
            -name=>'search_term',
            -class=>'form-control',
        ),
        submit (            
            -name=>'Search!',
            -class=>"btn btn-default",
        ), 
        end_form, 
}

sub logout { 
    my $p = CGI::Cookie->new(
        -value   => '',
        -path    => '/',
        -expires => 'now',
    );

    my $u = CGI::Cookie->new(
        -value   => '',
        -path    => '/',
        -expires => 'now',
    );

}

sub loginPage {
    print start_form,
        hidden ('browse_page', $browsePage), 
        textfield('login'), 
        password_field('password'),
        submit(
            -name=>'Begin!',
            -class=>"btn btn-default",
        ),  
        end_form,
}



sub gologout { 
    logout();
    return
        start_form,
        hidden ('home_page', 'true'), 
        submit(
            -name=>'Logout!',
            -class=>"btn btn-danger",
        ),  
        end_form, 
}



