% Fix landsat image issue
fprintf('Fixing landsat imagery: normalizing...\n')

% get paths, default file format being geotiff
path = pwd;
path1 = fullfile(path,'IndianVillagesDataset_DATA/imagery');
path0 = fullfile(path,'IndianVillagesDataset_DATA/masks');
path2 = fullfile(path,'display');
ext = '*.tif';

files = [];
files = [files, dir(fullfile(path1,ext))];

% conversion from single to normalized double
fprintf('|     Progress     |\n')
progressIntervals = ceil(length(files)/20);
for i=1:50
    map=imread(fullfile(path1,files(i).name),1);
    mask=imread(fullfile(path0,files(i).name),1);
    mask(mask~=0)=1;
    im=imadjust(map(:,:,4:-1:2),[0,0.35],[0,1],1.3);
    
    im(:,:,1)=im(:,:,1).*mask;
    im(:,:,2)=im(:,:,2).*mask;
    im(:,:,3)=im(:,:,3).*mask;
    
    nn=files(i).name;
    imwrite(double(im),fullfile(path2,[nn(1:end-4),'_m',nn(end-3:end)]))
    if i~=1 && ~mod(i-1,progressIntervals)
    	fprintf('|')
    end
end
fprintf('|\n')
msg = [num2str(length(files)),' images done!\n'];
fprintf(msg)

%quit