/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 22:03:23 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/09 22:34:22 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
//#include <stddef.h>
#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	size_t				i;
	unsigned char		*ptr1;
	const unsigned char	*ptr2;

	i = 0;
	if (!dest && !src)
		return (NULL);
	ptr1 = (unsigned char *)dest;
	ptr2 = (const unsigned char *)src;
	if (ptr1 > ptr2)
	{
		while (n-- > 0)
			ptr1[n] = ptr2[n];
	}
	else
	{
		while (i < n)
		{
			ptr1[i] = ptr2[i];
			i++;
		}
	}
	return (dest);
}

/*int	main(void)
{
	char	src[] = "Hello my name is mastoof";
	char	dest[24];
	size_t	n;

	n = 24;
	ft_memmove(dest, src, n);
	printf("Original: %s\n", src);
	printf("Copy: %s\n", dest);
}*/