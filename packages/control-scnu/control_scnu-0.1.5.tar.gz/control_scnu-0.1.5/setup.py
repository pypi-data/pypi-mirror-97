import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="control_scnu", # Replace with your own username
    version="0.1.5",
    author="lxy",
    author_email="2471974739@qq.com",
    description="A small example package20200805_lxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='<3.8',
    data_files=[('class\ txt',['API_KEY.txt', 'APP_ID.txt', 'SECRET_KEY.txt']),
                ('class\ speech', ['ardio.mp3']),
                ('class\ model', ['eye.xml', 'face.xml', '8hao_1.proto',
                                  'finally.proto', 'lxy1007.proto',
                                  'num_direction.proto','laji.proto']),
                ('class\ camera_pos',['bucket_hat.jpg', 'diadema.jpg',
                                      'medical_mask.jpg',  'N95.jpg',
                                      'peaked_cap.jpg','straw.jpg']),
                ('class\ picture', ['1.png']),
                ('class\ audio',['']),],
    include_package_data=True,

)
