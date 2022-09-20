import argparse
import random
import math
from PIL.ExifTags import TAGS
from PIL import ImageOps
from PIL import Image
import pandas as pd
import time
import helper

# got idea from https://medium.com/@jtreitz/the-algorithm-for-a-perfectly-balanced-photo-gallery-914c94a5d8af
# start partition problem algorithm from https://stackoverflow.com/a/7942946
# modified to act on list of images rather than the weights themselves
# more info on the partition problem http://www8.cs.umu.se/kurser/TDBAfl/VT06/algorithms/BOOK/BOOK2/NODE45.HTM

from operator import index, itemgetter

from pandas.core.dtypes.missing import notnull

def linear_partition(seq, k, dataList = None):
    if k <= 0:
        return []
    n = len(seq) - 1
    if k > n:
        return map(lambda x: [x], seq)
    table, solution = linear_partition_table(seq, k)
    k, ans = k-2, []
    if dataList == None or len(dataList) != len(seq):
        while k >= 0:
            ans = [[seq[i] for i in range(solution[n-1][k]+1, n+1)]] + ans
            n, k = solution[n-1][k], k-1
        ans = [[seq[i] for i in range(0, n+1)]] + ans
    else:
        while k >= 0:
            ans = [[dataList[i] for i in range(solution[n-1][k]+1, n+1)]] + ans
            n, k = solution[n-1][k], k-1
        ans = [[dataList[i] for i in range(0, n+1)]] + ans
    return ans

def linear_partition_table(seq, k):
    n = len(seq)
    table = [[0] * k for x in range(n)]
    solution = [[0] * (k-1) for x in range(n-1)]
    for i in range(n):
        table[i][0] = seq[i] + (table[i-1][0] if i else 0)
    for j in range(k):
        table[0][j] = seq[0]
    for i in range(1, n):
        for j in range(1, k):
            table[i][j], solution[i-1][j-1] = min(
                ((max(table[x][j-1], table[i][0]-table[x][0]), x) for x in range(i)),
                key=itemgetter(0))
    return (table, solution)

# end partition problem algorithm

def clamp(v,l,h):
    return l if v < l else h if v > h else v

# takes list of PIL image objects and returns the collage as a PIL image object
def makeCollage(imgList, spacing = 0, antialias = False, background=(0,0,0), aspectratiofactor = 1.0):
    # first downscale all images according to the minimum height of any image
    minHeight = min([img.height for img in imgList])
    if antialias:
        imgList = [img.resize((int(img.width / img.height * minHeight),minHeight), Image.ANTIALIAS) if img.height > minHeight else img for img in imgList]
    else:
        imgList = [img.resize((int(img.width / img.height * minHeight),minHeight)) if img.height > minHeight else img for img in imgList]
    
    # generate the input for the partition problem algorithm
    # need list of aspect ratios and number of rows (partitions)
    imgHeights = [img.height for img in imgList]
    totalWidth = sum([img.width for img in imgList])
    avgWidth = totalWidth / len(imgList)
    targetWidth = avgWidth * math.sqrt(len(imgList) * aspectratiofactor)
    
    numRows = clamp(int(round(totalWidth / targetWidth)), 1, len(imgList))
    if numRows == 1:
        imgRows = [imgList]
    elif numRows == len(imgList):
        imgRows = [[img] for img in imgList]
    else:
        aspectRatios = [int(img.width / img.height * 100) for img in imgList]
    
        # get nested list of images (each sublist is a row in the collage)
        imgRows = linear_partition(aspectRatios, numRows, imgList)
    
        # scale down larger rows to match the minimum row width
        rowWidths = [sum([img.width + spacing for img in row]) - spacing for row in imgRows]
        minRowWidth = min(rowWidths)
        rowWidthRatios = [minRowWidth / w for w in rowWidths]
        if antialias:
            imgRows = [[img.resize((int(img.width * widthRatio), int(img.height * widthRatio)), Image.ANTIALIAS) for img in row] for row,widthRatio in zip(imgRows, rowWidthRatios)]
        else:
            imgRows = [[img.resize((int(img.width * widthRatio), int(img.height * widthRatio))) for img in row] for row,widthRatio in zip(imgRows, rowWidthRatios)]
    
    # pupulate new image
    rowWidths = [sum([img.width + spacing for img in row]) - spacing for row in imgRows]
    rowHeights = [max([img.height for img in row]) for row in imgRows]
    minRowWidth = min(rowWidths)
    w,h = (minRowWidth, sum(rowHeights) + spacing * (numRows - 1))
    
    if background == (0,0,0):
        background += tuple([0])
    else:
        background += tuple([255])
    outImg = Image.new("RGBA", (w,h), background)
    xPos,yPos = (0,0)
    
    for row in imgRows:
        for img in row:
            outImg.paste(img, (xPos,yPos))
            xPos += img.width + spacing
            continue
        yPos += max([img.height for img in row]) + spacing
        xPos = 0
        continue
    
    return outImg


def getRandomRows(df, n):
    return df.ix[random.sample(df.index, n)]


def getNamesFromCsvForVarietyCollage():
    csv_cols = ['camnr', 'sequenznr', 'usecase', 'timestamp']
    csv_df = pd.read_csv('output/contents.csv', usecols= csv_cols)
    my_list = []

    df_usecase_1 = csv_df.loc[csv_df['usecase'] == 'lecturer']
    if df_usecase_1.empty == False:
        df_usecase_1 = df_usecase_1.sample().iloc[0]
        my_list.append(str(df_usecase_1['sequenznr']) + '_' + df_usecase_1['usecase'] + '.jpeg')

    df_usecase_2 = csv_df.loc[csv_df['usecase'] == 'persons_from_behind']
    if df_usecase_2.empty == False:
        df_usecase_2 = df_usecase_2.sample().iloc[0]
        my_list.append(str(df_usecase_2['sequenznr']) + '_' + df_usecase_2['usecase'] + '.jpeg')
    
    df_usecase_3 = csv_df.loc[csv_df['usecase'] == 'persons_from_front']
    if df_usecase_3.empty == False:
        df_usecase_3 = df_usecase_3.sample().iloc[0]
        my_list.append(str(df_usecase_3['sequenznr']) + '_' + df_usecase_3['usecase'] + '.jpeg')
    
    df_usecase_4 = csv_df.loc[csv_df['usecase'] == 'relevant_text']
    if df_usecase_4.empty == False:
        df_usecase_4 = df_usecase_4.sample().iloc[0]
        my_list.append(str(df_usecase_4['sequenznr']) + '_' + df_usecase_4['usecase'] + '.jpeg')

    df_usecase_5 = csv_df.loc[csv_df['usecase'].str.startswith('non_lecture_relevant_object_')]
    if df_usecase_5.empty == False:
        df_usecase_5 = df_usecase_5.sample().iloc[0]
        my_list.append(str(df_usecase_5['sequenznr']) + '_' + df_usecase_5['usecase'] + '.jpeg')
    
    return my_list


def getNamesFormCsvForPersonCollage():
    csv_cols = ['camnr', 'sequenznr', 'usecase', 'timestamp']
    csv_df = pd.read_csv('output/contents.csv', usecols= csv_cols)
    my_list = []

    df_usecase_1 = csv_df.loc[csv_df['usecase'] == 'lecturer']
    if df_usecase_1.empty == False:
        df_usecase_1 = df_usecase_1.sample(frac=1).reset_index(drop=True)
        my_list.append(str(df_usecase_1.iloc[0]['sequenznr']) + '_' + df_usecase_1.iloc[0]['usecase'] + '.jpeg')
        if(len(df_usecase_1.index) > 1):
            my_list.append(str(df_usecase_1.iloc[1]['sequenznr']) + '_' + df_usecase_1.iloc[1]['usecase'] + '.jpeg')

    df_usecase_2 = csv_df.loc[csv_df['usecase'] == 'persons_from_behind']
    if df_usecase_2.empty == False:
        df_usecase_2 = df_usecase_2.sample(frac=1).reset_index(drop=True)
        my_list.append(str(df_usecase_2.iloc[0]['sequenznr']) + '_' + df_usecase_2.iloc[0]['usecase'] + '.jpeg')
        #if(len(df_usecase_2.index) > 1):
        #    my_list.append(str(df_usecase_2.iloc[1]['sequenznr']) + '_' + df_usecase_2.iloc[1]['usecase'] + '.jpeg')
    
    df_usecase_3 = csv_df.loc[csv_df['usecase'] == 'persons_from_front']
    if df_usecase_3.empty == False:
        df_usecase_3 = df_usecase_3.sample(frac=1).reset_index(drop=True)
        my_list.append(str(df_usecase_3.iloc[0]['sequenznr']) + '_' + df_usecase_3.iloc[0]['usecase'] + '.jpeg')
        #if(len(df_usecase_3.index) > 1):
        #    my_list.append(str(df_usecase_3.iloc[1]['sequenznr']) + '_' + df_usecase_3.iloc[1]['usecase'] + '.jpeg')
    
    return my_list


def getNamesFormCsvForEnvCollage():
    csv_cols = ['camnr', 'sequenznr', 'usecase', 'timestamp']
    csv_df = pd.read_csv('output/contents.csv', usecols= csv_cols)
    my_list = []

    df_usecase_4 = csv_df.loc[csv_df['usecase'] == 'relevant_text']
    if df_usecase_4.empty == False:
        df_usecase_4 = df_usecase_4.sample(frac=1).reset_index(drop=True)
        my_list.append(str(df_usecase_4.iloc[0]['sequenznr']) + '_' + df_usecase_4.iloc[0]['usecase'] + '.jpeg')
        if(len(df_usecase_4.index) > 1):
            my_list.append(str(df_usecase_4.iloc[1]['sequenznr']) + '_' + df_usecase_4.iloc[1]['usecase'] + '.jpeg')
    
    df_usecase_5 = csv_df.loc[csv_df['usecase'].str.startswith('non_lecture_relevant_object_')]
    if df_usecase_5.empty == False:
        df_usecase_5 = df_usecase_5.sample(frac=1).reset_index(drop=True)
        my_list.append(str(df_usecase_5.iloc[0]['sequenznr']) + '_' + df_usecase_5.iloc[0]['usecase'] + '.jpeg')
        if(len(df_usecase_5.index) > 1):
            my_list.append(str(df_usecase_5.iloc[1]['sequenznr']) + '_' + df_usecase_5.iloc[1]['usecase'] + '.jpeg')
    
    return my_list


def loadPhotos(images, args):
    pilImages = []
    for f in images:
        img = Image.open('output/' + f)
        # Need to explicitly tell PIL to rotate image if EXIF orientation data is present
        exif = img.getexif()
        # Remove all exif tags
        for k in exif.keys():
            if k != 0x0112:
                exif[k] = None # If I don't set it to None first (or print it) the del fails for some reason. 
                del exif[k]
        # Put the new exif object in the original image
        new_exif = exif.tobytes()
        img.info["exif"] = new_exif
        # Rotate the image
        img = ImageOps.exif_transpose(img)
        if args.initheight > 2 and img.height > args.initheight:
            if args.noantialias:
                pilImages.append(img.resize((int(img.width / img.height * args.initheight),args.initheight)))
            else:
                pilImages.append(img.resize((int(img.width / img.height * args.initheight),args.initheight), Image.ANTIALIAS))
        else:
            pilImages.append(img)
    return pilImages


def saveCollage(collage, args, collageFileName):
    if args.width > 0 and collage.width > args.width:
        collage = collage.resize((args.width, int(collage.height / collage.width * args.width)), Image.ANTIALIAS)
        pass
    elif args.height > 0 and collage.height > args.height:
        collage = collage.resize((int(collage.width / collage.height * args.height), args.height), Image.ANTIALIAS)
        pass
    
    collage.save('output/'+ collageFileName + '.png')

def doCollageWithGivenNames(images, args, collageFileName):
    if len(images) < 2:
        print("Need to use 2 or more images. Try again")
        return                
    
    if args.shuffle:
        random.shuffle(images)
    else:
        images.sort() # by filename
    
    if args.count > 1:
        images = images[:args.count]      
        
    ##print('Loading photos...')
    pilImages = loadPhotos(images, args)
 
    ##print('Making collage...')
    collage = makeCollage(pilImages, args.imagegap, not args.noantialias, args.background, args.aspectratiofactor)

    saveCollage(collage, args, collageFileName)
    print('Collage is ready: ' + collageFileName)


def main():
    def rgb(s):
        try:
            rgb = (0 if v < 0 else 255 if v > 255 else v for v in map(int, s.split(',')))
            return rgb
        except:
            raise argparse.ArgumentTypeError('Background must be (r,g,b) --> "(0,0,0)" to "(255,255,255)"')
    parse = argparse.ArgumentParser(description='Photo collage maker')
    parse.add_argument('-W', '--width', dest='width', type=int, help='resulting collage image height (mutually exclusive with --height)', default=1080)
    parse.add_argument('-H', '--height', dest='height', type=int, help='resulting collage image height (mutually exclusive with --width)', default=1920)
    parse.add_argument('-i', '--initheight', dest='initheight', type=int, help='resize images on input to set height', default=1080)
    parse.add_argument('-s', '--shuffle', action='store_true', dest='shuffle', help='enable images shuffle')
    parse.add_argument('-g', '--gap-between-images', dest='imagegap', type=int, help='number of pixels of transparent space (if saving as png file; otherwise black or specified background color) to add between neighboring images', default=3)
    parse.add_argument('-b', '--background-color', dest='background', type=rgb, help='color (r,g,b) to use for background if spacing is added between images', default=(0,0,0))
    parse.add_argument('-c', '--count', dest='count', type=int, help='count of images to use', default=0)
    parse.add_argument('-r', '--scale-aspect-ratio', dest='aspectratiofactor', type=float, help='aspect ratio scaling factor, multiplied by the average aspect ratio of the input images to determine the output aspect ratio', default=0.5)
    parse.add_argument('-a', '--no-antialias-when-resizing', dest='noantialias', action='store_false', help='disable antialiasing on intermediate resizing of images (runs faster but output image looks worse; final resize is always antialiased)')
    args = parse.parse_args()


    print('Start Collage Variety..')
    varietyImages = getNamesFromCsvForVarietyCollage()
    doCollageWithGivenNames(varietyImages, args, 'collageVariety_'+ time.strftime('%H%M%S', helper.getLocalTime(time.time())))

    print('Start Collage Person..')
    personImages = getNamesFormCsvForPersonCollage()
    doCollageWithGivenNames(personImages, args, 'collagePerson_'+ time.strftime('%H%M%S', helper.getLocalTime(time.time())))

    print('Start Collage Environment..')
    envImages = getNamesFormCsvForEnvCollage()
    doCollageWithGivenNames(envImages, args, 'collageEnvironment'+ time.strftime('%H%M%S', helper.getLocalTime(time.time())))


if __name__ == '__main__':
    main()