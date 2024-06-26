import argparse
import os
import shutil
from bs4 import BeautifulSoup
import numpy as np
import cv2
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

class ConvertPageXmlToBinaryMask:
    def __init__(self, InputDir, OutputDir, DeletePrevious):
        self.InputDir = InputDir
        self.OutputDir = OutputDir
        self.DeletePrevious = DeletePrevious

        if self.DeletePrevious:
            shutil.rmtree(self.OutputDir, ignore_errors=True)
            os.makedirs(self.OutputDir, exist_ok=True)

    def GetFileNames(self):
        ImageNames = []
        pageXmls = []

        for file in os.listdir(self.InputDir):
            if file.endswith(".jpg"):
                ImageNames.append(file)
            if file.endswith(".xml"):
                pageXmls.append(file)

        return ImageNames, pageXmls
    
    def ParsePageXml(self, pageXml):
        with open(pageXml, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        soup = BeautifulSoup(xml_content, 'xml')
        return soup

    def GetPageMetaData(self, soup):
        for page in soup.find_all('Page'):
            Name = page['imageFilename']
            Height = page['imageHeight']
            Width = page['imageWidth']
        
        return {'imageFilename': Name, 'imageHeight': Height, 'imageWidth': Width}
    
    def DrawTextLines(self, soup, Height, Width):
        mask = np.zeros((int(Height), int(Width), 3), dtype=np.uint8)
        
        for textline in soup.find_all('TextLine'):
            coords = textline.Coords['points']
            points = [tuple(map(int, point.split(','))) for point in coords.split()]
            
            cv2.fillPoly(mask, [np.array(points)], color=(255, 255, 255))
            cv2.polylines(mask, [np.array(points)], isClosed=True, color=(0, 0, 0), thickness=4)

        mask_image = Image.fromarray(mask)
        return mask_image
    
    def SaveBinaryMask(self, mask_image, OutputDir, Name):
        mask_image.save(os.path.join(OutputDir, Name + '.png'))

    def ProcessPageXml(self, pageXml):
        Name = pageXml.split('.')[0]
        ImageName = Name + '.jpg'
        ImagePath = os.path.join(self.InputDir, ImageName)
        pageXmlPath = os.path.join(self.InputDir, pageXml)

        soup = self.ParsePageXml(pageXmlPath)
        PageMetaData = self.GetPageMetaData(soup)
        Height = PageMetaData['imageHeight']
        Width = PageMetaData['imageWidth']

        mask_image = self.DrawTextLines(soup, Height, Width)
        self.SaveBinaryMask(mask_image, self.OutputDir, Name)

        return f"Processed {pageXml}"

    def Convert(self):
        ImageNames, pageXmls = self.GetFileNames()

        # Using ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.ProcessPageXml, pageXml) for pageXml in pageXmls]
            
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing PageXml Files"):
                result = future.result()
                tqdm.write(result)

        print("All Binary Masks saved successfully")
        #print number of files processed and xmls and images
        print(f"Total Images: {len(ImageNames)}")
        print(f"Total PageXmls: {len(pageXmls)}")
        print(f"Total Binary Masks: {len(os.listdir(self.OutputDir))}")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert PageXml to Binary Mask")
    parser.add_argument('-i', '--InputDir', type=str, default="Dataconverstion", help='Input Directory containing PageXml files', required=False)
    parser.add_argument('-o', '--OutputDir', type=str, default="ProcessedData", help='Output Directory containing Binary Mask files', required=False)
    parser.add_argument('-d', '--DeletePrevious', type=bool, default=True, help='Delete the previous Output Directory', required=False)

    args = parser.parse_args()
    converter = ConvertPageXmlToBinaryMask(args.InputDir, args.OutputDir, args.DeletePrevious)
    converter.Convert()
