depends = ('ITKPyBase', 'ITKTransform', 'ITKDisplacementField', 'ITKCommon', )
templates = (
  ('TransformFileReaderTemplate', 'itk::TransformFileReaderTemplate', 'itkTransformFileReaderTemplateD', False, 'double'),
  ('TransformFileReaderTemplate', 'itk::TransformFileReaderTemplate', 'itkTransformFileReaderTemplateF', False, 'float'),
  ('TransformFileWriterTemplate', 'itk::TransformFileWriterTemplate', 'itkTransformFileWriterTemplateD', False, 'double'),
  ('TransformFileWriterTemplate', 'itk::TransformFileWriterTemplate', 'itkTransformFileWriterTemplateF', False, 'float'),
  ('TransformIOBaseTemplate', 'itk::TransformIOBaseTemplate', 'itkTransformIOBaseTemplateD', False, 'double'),
  ('TransformIOBaseTemplate', 'itk::TransformIOBaseTemplate', 'itkTransformIOBaseTemplateF', False, 'float'),
)
