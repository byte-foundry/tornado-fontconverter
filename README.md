tornado-fontconverter
=====================

placeholder for our future tornado+libfontforge based font converter

We choose to use Vagrant with Azure to mount completely our VM.
- Install Vagrant on your OS.

- Install Azure plugin for Vagrant : vagrant plugin install azure
#####    IMPORTANT FOR MAC OS X USERS:  
You may encounter some issues installing the plugin. 
If you're using MacOS X (problem encountered on 10.7.5 Lion), you may have to re-install properly the following librairies : libxml2,libxslt, libiconv in order to install nokogiri. 
Nokogiri may also have problems running because of Xcode Command Line Tools, you have to authorized them on Xcode, and sometimes upgrade your Xcode version to 4.6.3 or higher. 
And you may also install a more stable version of Ruby, following this workaround: http://deanclatworthy.com/2012/12/how-to-fix-hanging-gem-install-on-a-fresh-osx-lion-install

#####    IMPORTANT FOR UBUNTU USERS :
Ruby2.0 isn't available by default on Ubuntu 14.04 (see bug https://bugs.launchpad.net/ubuntu/+source/ruby2.0/+bug/1310292 ) 
You need the following workaround: http://blog.costan.us/2014/04/restoring-ruby-20-on-ubuntu-1404.html 
Or to type this command line : curl -L https://get.rvm.io | bash -s stable --ruby 
And don't skip the last instruction: "To start using RVM you need to run source /home/{username}/.rvm/scripts/rvm"

- vagrant init : will create a Vagrantfile with only comments. You should edit this file afterwards.
- Edit your Vagrantfile with the different fields you need. It should look like the one in this link :
http://hypernephelist.com/2014/06/18/php-dev-box-with-vagrant.html
If you are likely to create several VMs with different images, only the azure.vm.image field will change. Plus, if you want to load another box, you must not edit your Vagrantfile either, but only the instruction vagrant box (which we will explain below).

- vagrant box add [...]
Depending on which type of box you want to use. For Azure boxes, we recommand https://github.com/msopentech/vagrant-azure/raw/master/dummy.box (therefore you can give you the name you want, the same in override.vm.box field in Vagrantfile)

- Scripting :
If you want to use a script and provision your VM with, add before the last 'end' instruction a line with config.vm.provision :shell, :path => "<your script path>". 
Plus, if you choose to share folders with your local machine, you can specify it in your Vagranfile before vagrant up-ing.

- Up : 
	vagrant up --provider=azure (if you are using Azure, unless vagrant up only)
	It will create your VM with the configuration you notified in Vagrantfile (folder sharing, port-forwarding, provisiining and so on), and provision it if necessary.
	While you don't change your Vagrantfile, you will not need to vagrant reload. For example, if you change your provision script, just type vagrant provision command-line to apply changes.
	
- If any of these points fail, the best way to solve the problem is surely to restart on a fresh VM. To do that, keep a copy in your Vagrantfile somewhere (in a Vagrantfile-old for example) and launch the following script:
	vagrant destroy --force
	vagrant box remove --force <your box name>
	rm vagrantfile
	vagrant init
	cat Vagrantfile-old > Vagrantfile    #you may apply changes afterwards here if you have some Vagrant configuration issues
	vagrant box add <your box name> <your box url>
	vagrant up [--provider=yourprovider if needed, VirtualBox by default]
